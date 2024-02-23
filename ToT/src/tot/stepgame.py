import os
import re
import pandas as pd
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.stepgame import * 

def get_current_chains(y: str) -> str:
    last_line = y.strip().split('\n')[-1] # last generated thought
    return last_line

def is_target_in_chain(chain_str):
    # Extract the part before the arrow
    chain_pattern = re.search(r'chain: (.+?),', chain_str)
    target_pattern = re.search(r'target: (\w+),', chain_str)   
    if chain_pattern and target_pattern:
        target = target_pattern.group(1)   
        chain = chain_pattern.group(1)    
        chain_parts = chain.split('->')
        second_last_part = chain_parts[-2].strip()
        # Get the last object in the chain
        last_object = second_last_part.split()[0]      
        # Compare it with the target
        return last_object == target
    return False


class StepgameTask:
    def __init__(self, file=''): #qa3_test.txt
    	super().__init__()
    	path = os.path.join(DATA_PATH, 'stepgame', 'correct_clean', file)
    	print(path)
    	self.data = []
    	self.label = []
    	with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    	inp = ''
    	self.n = 0
    	for line in lines:   
            _, line = line.strip().split(' ', 1)
            if line.find("What is the relation") == -1:
                line = _ + '. ' + line 
            if line.endswith('1'):
                self.n += 1
                line, target, _ = line.split('\t')
                inp += line + ' ' 
                #self.data.append([[inp],[target]])
                self.data.append(inp)
                self.label.append(target)
                inp = ''
            else:
                inp += line + ' '  
	
    	self.value_cache = {}
    	self.steps = 10
    	self.stops = ['\n'] * 3
	
    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        return output.strip().split('\n')[-1].replace('Answer: ', '').split('=')[0]
        # numbers = re.findall(r'\d+', expression)
        # problem_numbers = re.findall(r'\d+', self.data[idx])
        # if sorted(numbers) != sorted(problem_numbers):
        #     return {'r': 0}
        # try:
        #     # print(sympy.simplify(expression))
        #     return {'r': int(sympy.simplify(expression) == 24)}
        # except Exception as e:
        #     # print(e)
        #     return {'r': 0}
            
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        current_chains = get_current_chains(y if y else x)
        print('curent chains:\n',current_chains )
        if y=='':
            prompt = propose_first_step_prompt.format(input=x)
        elif is_target_in_chain(current_chains) == True:
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
        else:
            prompt = propose_prompt.format(input=current_chains)
        return prompt
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        first_line = y.strip().split('\n')[0]
        last_line = y.strip().split('\n')[-1]
        # if 'Answer: '  in last_line:  # last step
        #     ans = last_line.lower().replace('answer: ', '')
        #     # print([value_last_step_prompt.format(input=x, answer=ans)])
        #     return value_last_step_prompt.format(input=first_line, answer=ans)
        current_chains = get_current_chains(y)
        return value_prompt.format(input=current_chains)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        print("y:::",len(y.strip().split('\n')), y)
        if len(y.strip().split('\n')) == len(re.findall(r'\b\d+\.\s', x)) and 'answer' not in y.lower():
            return 0
        if 'answer' in y.lower():
            return 200
        # if 'no ' in y.lower():
        #     return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value        
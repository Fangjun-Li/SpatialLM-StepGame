import argparse
from collections import defaultdict
import sys
import os
import pandas as pd
from tqdm import tqdm
sys.path.append('../')
import json
from pipeline_base import ToTCoTline

class StepGame(ToTCoTline):
    # take a dataset file in csv and return #correct and #total
    def eval_dataset(self, path_to_dataset, max_num=None):
        file_name = os.path.splitext(os.path.basename(path_to_dataset))[0]
        correct, total = defaultdict(int), 0
        # read in the dataset
        with open(path_to_dataset, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # each example is a mapping from name (str) to [INPUT] sentences (str)
        inp = ''
        chain=''
        for line in lines:
            _, line = line.strip().split(' ', 1)
            
            ##########key
            if line.find("What is the relation") == -1:
                line = _ + '. ' + line      
            ##########key
            if line.endswith('1'):
                line, target, _ = line.split('\t')
                inp += line
                example = {name: inp for name in self.prompt}
                
                
                # Read the JSON file
                with open(f'ToT/logs/stepgame/{file_name}.json', "r") as file:
                    tot_data = json.load(file)
                
                # Extract strings after "Answer: " from the "ys" key based on idx
                answers = []
                for entry in tot_data:
                    if entry['idx'] == total:
                        for ys in entry['ys']:
                            if "Answer: " in ys:
                                chain = ys.split("Answer: ")[1].strip()
                # print(inp)
                # print(chain)
                response = self.eval_single_example(example, chain)
                total += 1
                for name in response:   
                    if name == 'ToT_CoT':
                        prediction = response[name].split('Answer:')[-1].strip()
                    else:
                        prediction = response[name].split('answer is')[-1].strip().strip('.') if 'CoT' in name else response[name].strip()
                    # sol = 1 if target in prediction else 0
                    sol = 1 if target == prediction else 0
                    
                    correct[name] += sol
                    # record the mistake
                    if sol == 0:
                        if self.debug:
                            breakpoint()
                        self.mistakes.append((
                            path_to_dataset,
                            total,
                            inp,
                            target,
                            name,
                            response[name]))
                inp = ''
            else:
                inp += line + '\n'
            if max_num and total == max_num:
                break
        return correct, total

def main(args):
    pipeline = StepGame(vars(args))
    # 1. Load the prompt, which we call base
    # (one can test multiple versions of prompts by adding, e.g., 'base2': PATH)
    path_prompt = {
        'ToT_CoT': 'prompts/ToT_CoT.txt',    
        }
    pipeline.load_prompt(path_prompt)
    # 2. Load the cache for GPT-3 response to avoid duplicated query
    pipeline.path_cache = {
        name: f'cached_responses/correct_clean/ToT_CoT/{name}_{pipeline.engine}_4shot_prompt_20.pickle'
        for name in path_prompt}
    pipeline.load_cache()
    # 3. Evaluate on test data
    max_num = args.num # maximum number of data to be evaluated per file
    path_test_data_files = [       
        # 'data/correct_clean/qa1_test.txt',
        # 'data/correct_clean/qa2_test.txt',
        'data/correct_clean/qa3_test.txt',
        'data/correct_clean/qa4_test.txt',
        'data/correct_clean/qa5_test.txt',
        'data/correct_clean/qa6_test.txt',
        'data/correct_clean/qa7_test.txt',
        'data/correct_clean/qa8_test.txt',
        'data/correct_clean/qa9_test.txt',
        'data/correct_clean/qa10_test.txt',
    ]
    correct, total = defaultdict(int), 0
    print('name    \tacc\tcorrect\ttotal\tfile_name')
    for file in path_test_data_files:
        _correct, _total = pipeline.eval_dataset(file, max_num)
        for name in pipeline.prompt:
            print(f'{name: <8}\t{100*_correct[name]/_total:.2f}\t{_correct[name]}\t{_total}\t{file}')
            correct[name] += _correct[name]
            # print(_correct[name])
        total += _total
    for name in pipeline.prompt:
        print(f'{name: <8}\t{100*correct[name]/total:.2f}\t{correct[name]}\t{total}\tAll')

    # 5. record the mistakes
    # mistake_cols = ['file', 'index', 'example', 'target', 'prompt name', 'response']
    # pipeline.save_mistakes(mistake_cols)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', default=20, type=int,
        help='maximum number of data to be evaluated per file')
    # gpt-35-turbo
    parser.add_argument('--engine', default="gpt-4", type=str,
        help='the engine name in \{gpt-4, gpt-35-turbo, text-davinci-003, text-curie-001\}')
    parser.add_argument('--path_mistakes', default='cached_responses/correct_clean/ToT_CoT/mistakes.xlsx', type=str,
        help='the file that records mistakes')
    parser.add_argument('--debug', default=False, action='store_true', help='debug mode')
    args = parser.parse_args()
    main(args)

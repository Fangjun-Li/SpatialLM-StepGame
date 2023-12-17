import argparse
from collections import defaultdict
import sys
import pandas as pd
from tqdm import tqdm
import os
import pickle
sys.path.append('../')

from pipeline_base import Baseline

class StepGame(Baseline):
    def load_cache(self):
        for kind in self.path_cache:
            if os.path.isfile(self.path_cache[kind]):
                with open(self.path_cache[kind], 'rb') as f:
                    self.cache[kind] = pickle.load(f)
            else:
                self.cache[kind] = {}
    
    def load_prompt(self, kind_to_path):
        self.prompt={}
        for kind in kind_to_path:
            with open(kind_to_path[kind], 'r', encoding='utf-8') as f:
                self.prompt[kind] = f.read()
        # print(self.prompt)
    
    # take a dataset file in csv and return #correct and #total
    def eval_dataset(self, path_to_dataset, max_num=None):
        correct, total = defaultdict(int), 0
        # read in the dataset
        with open(path_to_dataset, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # each example is a mapping from name (str) to [INPUT] sentences (str)
        inp = ''
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
                response = self.eval_single_example(example)
                total += 1
                for name in response:
                    # if name == 'our_CoT_5shot' :
                    #     print("response[name]:",response[name])
                    prediction = response[name].split('Answer:')[-1].strip() if 'base' not in name else response[name].strip()
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
    prompt_type = args.prompt_type
    
    if prompt_type == 'base_5shot':
        path_prompt_all = {
            **{f'base_5shot_{i}': f'prompts/separate/baseline_5shot_clean{i}.txt' for i in range(1, 11)},
        }
        pipeline.path_cache = { 
            'base_5shot': f'cached_responses/correct_clean/5shot_seperate/base_{pipeline.engine}_clean_seperate_prompt_1000.pickle',
            }
    elif prompt_type == 'our_CoT_5shot':
        path_prompt_all = {
            **{f'our_CoT_5shot_{i}': f'prompts/separate/Our_CoT_5shot_clean{i}.txt' for i in range(1, 11)},
        }
        pipeline.path_cache = { 
            'our_CoT_5shot': f'cached_responses/correct_clean/5shot_seperate/Our_CoT_{pipeline.engine}_clean_seperate_prompt_1000.pickle',
            }
    else:
        pass

    # pipeline.load_prompt(path_prompt)
    # 2. Load the cache for GPT-3 response to avoid duplicated query
    pipeline.load_cache()
    # 3. Evaluate on test data
    max_num = args.num # maximum number of data to be evaluated per file
    i_start=args.kstart
    i_end=args.kend
    path_test_data_files = [      
        f'data/correct_clean/qa{i}_test.txt' for i in range(i_start, i_end)
    ]
        
    correct, total = 0, 0
    print('name    \tacc\tcorrect\ttotal\tfile_name')
    for i, file in enumerate(path_test_data_files, start=i_start):
        if i == i_end:
            break
        else:          
            if prompt_type == 'base_5shot':
                path_prompt={'base_5shot': path_prompt_all[f'base_5shot_{i}'],}
            elif prompt_type == 'our_CoT_5shot':
                path_prompt={'our_CoT_5shot': path_prompt_all[f'our_CoT_5shot_{i}'],} 
            else:
                pass
            
            
            # print("path_prompt:",path_prompt)
            pipeline.load_prompt(path_prompt)
            _correct, _total = pipeline.eval_dataset(file, max_num)
            for name in pipeline.prompt:
                print(f'{name: <8}\t{100*_correct[name]/_total:.2f}\t{_correct[name]}\t{_total}\t{file}')
            correct += _correct[name]
                # print(_correct[name])
            total += _total
    for name in pipeline.prompt: 
        print(f'{name: <8}\t{100*correct/total:.2f}\t{correct}\t{total}\tAll')

    # 5. record the mistakes
    # mistake_cols = ['file', 'index', 'example', 'target', 'prompt name', 'response']
    # pipeline.save_mistakes(mistake_cols)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', default=100, type=int,
        help='maximum number of data to be evaluated per file')
    parser.add_argument('--kstart', default=1, type=int,
        help='start file')
    parser.add_argument('--kend', default=11, type=int,
        help='end file')
    parser.add_argument('--prompt_type', default='base_5shot', type=str,
        help='setting the type to prompts, base_5shot, our_CoT_5shot')
    # gpt-35-turbo
    parser.add_argument('--engine', default="gpt-35-turbo", type=str,
        help='the engine name in \{gpt-4, gpt-35-turbo, text-davinci-003, text-curie-001\}')
    parser.add_argument('--path_mistakes', default='cached_responses/correct_clean/5shot_seperate/mistakes.xlsx', type=str,
        help='the file that records mistakes')
    parser.add_argument('--debug', default=False, action='store_true', help='debug mode')
    args = parser.parse_args()
    main(args)

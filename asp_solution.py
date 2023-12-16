import os
import re
import pickle
import time
from clingo.control import Control
from clingo.symbol import parse_term
import pandas as pd
import openai
import argparse
import sys
sys.path.append('../')
from sentence_to_relation import sentence_to_relation


relation_to_facts = {
    r"(?P<obj1>\w+)_left_(?P<obj2>\w+)":r'left("\1", "\2").',
    r"(?P<obj1>\w+)_right_(?P<obj2>\w+)": r'right("\1", "\2").',
    r"(?P<obj1>\w+)_over_(?P<obj2>\w+)": r'top("\1", "\2").',
    r"(?P<obj1>\w+)_below_(?P<obj2>\w+)": r'down("\1", "\2").',
    r"(?P<obj1>\w+)_lowerleft_(?P<obj2>\w+)": r'down_left("\1", "\2").',
    r"(?P<obj1>\w+)_upperright_(?P<obj2>\w+)": r'top_right("\1", "\2").',
    r"(?P<obj1>\w+)_lowerright_(?P<obj2>\w+)": r'down_right("\1", "\2").',
    r"(?P<obj1>\w+)_upperleft_(?P<obj2>\w+)": r'top_left("\1", "\2").',
    r"(?P<obj1>\w+)_query_(?P<obj2>\w+)": r'query("\1", "\2").',
}



stepgame = '''
% assume the 2nd queried object is at location (0,0)
location(Q2, 0, 0) :- query(_, Q2).

% extract answer relation R such that the offset (Ox,Oy) of R is in the same direction of (X,Y)
answer(R) :- query(Q1, _), location(Q1, X, Y), offset(R, Ox, Oy),
    Ox=-1: X<0; Ox=0: X=0; Ox=1: X>0;
    Oy=-1: Y<0; Oy=0: Y=0; Oy=1: Y>0.
'''

location = '''
% general format translation, which can also be easily done in python script
% (this is not needed if we directly extract the general form in the beginning as in bAbI task4)
is(A, top, B) :- top(A, B).
is(A, top, B) :- up(A, B).
is(A, down, B) :- down(A, B).
is(A, left, B) :- left(A, B).
is(A, right, B) :- right(A, B).
is(A, top_left, B) :- top_left(A, B).
is(A, top_right, B) :- top_right(A, B).
is(A, down_left, B) :- down_left(A, B).
is(A, down_right, B) :- down_right(A, B).
is(A, east, B) :- east(A, B).
is(A, west, B) :- west(A, B).
is(A, south, B) :- south(A, B).
is(A, north, B) :- north(A, B).

% synonyms
synonyms(
    north, northOf; south, southOf; west, westOf; east, eastOf;
    top, northOf; down, southOf; left, westOf; right, eastOf
).
synonyms(A, B) :- synonyms(B, A).
synonyms(A, C) :- synonyms(A, B), synonyms(B, C), A!=C.

% define the offsets of 8 spacial relations
offset(
    overlap,0,0; top,0,1; down,0,-1; left,-1,0; right,1,0; 
    top_left,-1,1; top_right,1,1; down_left,-1,-1; down_right,1,-1
).

% derive the kind of spacial relation from synonyms and offset
is(A, R1, B) :- is(A, R2, B), synonyms(R1, R2).
is(A, R1, B) :- is(B, R2, A), offset(R2,X,Y), offset(R1,-X,-Y).

% derive the location of every object
% the search space of X or Y coordinate is within -100 and 100
% (to avoid infinite loop in clingo when data has error)
nums(-100..100).

location(A, Xa, Ya) :-
    location(B, Xb, Yb), nums(Xa), nums(Ya),
    is(A, Kind, B), offset(Kind, Dx, Dy),
    Xa-Xb=Dx, Ya-Yb=Dy.

location(B, Xb, Yb) :-
    location(A, Xa, Ya), nums(Xb), nums(Yb),
    is_on(A, Kind, B), offset(Kind, Dx, Dy),
    Xa-Xb=Dx, Ya-Yb=Dy.
'''

class Context:
    def gen_feature(self, x):
        ret = []
        for term in str(x.string).split(' '):
            ret.append(parse_term(term))
        return ret

class Pipeline:
    def __init__(self, args):
        self.asp_program = ''
        
        ###########
        # Cache
        ###########
        self.path_cache = {} # store the mapping from kind (str) to cache file (str)
        self.cache = {} # store the GPT3 facts for visited stories
        self.path_mistakes = 'mistakes.xlsx' # file to store the wrong pridictions
        self.mistakes = [] # store the wrong predictions

        for k,v in args.items():
            setattr(self, k, v)


    # take a sentence and its kind, return the fact
    def gen_fact(self, sentence):
        # generate and cache the fact in cache if it's not cached before
        mapped_relation = ''
        mapped_fact = ''
        
        for template, relation in list(sentence_to_relation.items()):
            if re.search(template, sentence):
                mapped_relation = re.sub(template, relation, sentence)
            
        for relation,fact in list(relation_to_facts.items()):
            if re.search(relation, mapped_relation):
                mapped_fact = re.sub(relation, fact, mapped_relation)

        return mapped_fact
    
    # take a list of GPT3 facts and return the answer set
    def gen_answer_set(self, facts, opt=False):
        """
        Args:
            facts (str): a string of ASP facts
            opt (bool): if true, only optimal answer sets are returned
                        leave it to False when there is no weak constraint
        """
        program = self.asp_program + facts
        clingo_control = Control(['0', '--warn=none', '--opt-mode=optN', '-t', '4'])
        models = []
        try:
            clingo_control.add('base', [], program)
            clingo_control.ground([('base', [])], context=Context())
        except:
            if self.debug:
                print(facts)
                breakpoint()
            return []
        if opt:
            clingo_control.solve(on_model = lambda model: models.append(model.symbols(atoms=True)) if model.optimality_proven else None)
        else:
            clingo_control.solve(on_model = lambda model: models.append(model.symbols(atoms=True)))
        models = [[str(atom) for atom in model] for model in models]
        return models

    # return the answer sets for an example data instance
    def eval_single_example(self, example, facts='', clean=False, opt=False):
        """
        Args:
            example (dict): a mapping from kind (str) to a list of sentences
            facts (str): additionally facts used during inference
            clean (bool): if true, remove all quotes turn all letters into lower case
        """
        fact = ''
        for kind in example:
            for sentence in example[kind]:
                fact += self.gen_fact(sentence)
        if clean:
            fact = fact.replace('\"', '').lower()
        # any dash between words should be replaced by underscore in clingo
        fact = fact.replace('-', '_')
        # answer_sets = self.gen_answer_set(fact + '\n\n' + facts, opt=opt)
        answer_sets = self.gen_answer_set(fact + '\n\n' + facts, opt=opt)
        return answer_sets, fact

    def save_mistakes(self, mistake_cols):
        df = pd.DataFrame(self.mistakes, columns=mistake_cols)
        df.to_excel(self.path_mistakes)



class StepGame(Pipeline):
    target_map = {
        'above': 'top',
        'below': 'down',
        'left': 'left',
        'right': 'right',
        'upper-left': 'top_left',
        'upper-right': 'top_right',
        'lower-left': 'down_left',
        'lower-right': 'down_right'
        }

    # take a dataset file in csv and return #correct and #total
    def eval_dataset(self, path_to_dataset, max_num=None):
        correct = 0
        total = 0
        # read in the dataset
        with open(path_to_dataset, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # each example is a mapping from kind (str) to list of sentences (str)
        example = {'location': []}
        for line in lines:
            _, line = line.strip().split(' ', 1)
            if line.endswith('1'):
                line, target, _ = line.split('\t')
                target_atom = f'answer({self.target_map.get(target, target)})'
                example['location'].append(line)
                answer_sets, fact = self.eval_single_example(example)
                sol = 1 if any([target_atom in answer_set for answer_set in answer_sets]) else 0
                correct += sol
                total += 1
                # record the mistake
                if sol == 0:
                    self.mistakes.append((
                        path_to_dataset,
                        total,
                        target,
                        '\n'.join(example['location']),
                        fact.replace('.', '.\n')[:-1]))
                example = {'location': []}
            else:
                example['location'].append(line)
            if max_num and total == max_num:
                break
        return correct, total

def main(args):
    pipeline = StepGame(vars(args))
    # 1. Set up the ASP program
    pipeline.asp_program = stepgame + location
    
    # 2. Evaluate on test data
    max_num = args.num # maximum number of data to be evaluated per file
    path_test_data_files = [
        'data/correct_clean/qa1_test.txt',
        'data/correct_clean/qa2_test.txt',
        'data/correct_clean/qa3_test.txt',
        'data/correct_clean/qa4_test.txt',
        'data/correct_clean/qa5_test.txt',
        'data/correct_clean/qa6_test.txt',
        'data/correct_clean/qa7_test.txt',
        'data/correct_clean/qa8_test.txt',
        'data/correct_clean/qa9_test.txt',
        'data/correct_clean/qa10_test.txt',
        
        'data/correct_noise/qa1_test.txt',
        'data/correct_noise/qa2_test.txt',
        'data/correct_noise/qa3_test.txt',
        'data/correct_noise/qa4_test.txt',
        'data/correct_noise/qa5_test.txt',
        'data/correct_noise/qa6_test.txt',
        'data/correct_noise/qa7_test.txt',
        'data/correct_noise/qa8_test.txt',
        'data/correct_noise/qa9_test.txt',
        'data/correct_noise/qa10_test.txt',
    ]
    correct = total = 0
    print('acc\t\tcorrect\t\ttotal\t\tfile_name')
    for file in path_test_data_files:
        _correct, _total = pipeline.eval_dataset(file, max_num)
        print(f'{100*_correct/_total:.2f}\t{_correct}\t\t\t{_total}\t\t{file}')
        correct += _correct
        total += _total
    print(f'{100*correct/total:.2f}\t{correct}\t\t\t{total}\t\tAll')

    # 3. record the mistakes
    mistake_cols = ['file', 'index', 'target', 'example', 'fact']
    pipeline.save_mistakes(mistake_cols)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', default=1000, type=int,
        help='maximum number of data to be evaluated per file')
    parser.add_argument('--path_mistakes', default='mistakes.xlsx', type=str,
        help='the file that records mistakes')
    parser.add_argument('--debug', default=False, action='store_true', help='debug mode')
    args = parser.parse_args()
    main(args)

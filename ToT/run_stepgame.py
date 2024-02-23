import os
import json
import argparse
import sys
import os
import openai
sys.path.insert(0,'./src')
from tot.tasks import get_task
from tot.methods.bfs import solve, naive_solve
from tot.models import gpt_usage


def run(args):
    task = get_task(args.task)
    logs, chains, cnt_avg, cnt_any = [], [], 0, 0
    file_hop = 'qa'+ args.task.split('_')[1]+'_test'
    # print(file_hop)
    if args.naive_run:
        file = f'./logs/stepgame/{file_hop}_{args.backend}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    else:
        file = f'./logs/stepgame/{file_hop}_{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    answerfile = f'./logs/{args.task}/{file_hop}.json'
    print("log file exists: ",os.path.exists(file))
    os.makedirs(os.path.dirname(file), exist_ok=True)

    for i in range(args.task_start_index, args.task_end_index):
        # solve
        if args.naive_run:
            ys, info = naive_solve(args, task, i) 
        else:
            ys, info = solve(args, task, i)

        # log
        infos = [task.test_output(i, y) for y in ys]
        info.update({'idx': i, 'ys': ys, 'infos': infos, 'usage_so_far': gpt_usage(args.backend)})
        # info.update({'idx': i, 'ys': ys, 'infos': infos, 'usage_so_far': 0})
        logs.append(info)
        chains.append({'idx': i, 'ys': ys, 'answers': infos, 'usage_so_far': gpt_usage(args.backend)})
        # chains.append({'idx': i, 'ys': ys, 'answers': infos, 'usage_so_far': 0})
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)
        with open(answerfile, 'w') as f:
            json.dump(chains, f, indent=4)
        # log main metric
    #     accs = [info['r'] for info in infos]
    #     cnt_avg += sum(accs) / len(accs)
    #     cnt_any += any(accs)
    #     print(i, 'sum(accs)', sum(accs), 'cnt_avg', cnt_avg, 'cnt_any', cnt_any, '\n')
    
    # n = args.task_end_index - args.task_start_index
    # print(cnt_avg / n, cnt_any / n)
    # print('usage_/so_far', gpt_usage(args.backend))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, choices=['gpt-4', 'gpt-35-turbo','text-davinci-003'], default='gpt-4')
    args.add_argument('--temperature', type=float, default=0.7)

    args.add_argument('--task', type=str, required=False,default='stepgame_5', choices=['game24', 'text', 'crosswords', 'stepgame'])
    args.add_argument('--task_start_index', type=int, default=0)
    args.add_argument('--task_end_index', type=int, default=1)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'])  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'],default='propose')
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'],default='value')
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy', 'drop'], default='greedy')
    args.add_argument('--n_generate_sample', type=int, default=1)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=3)

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)
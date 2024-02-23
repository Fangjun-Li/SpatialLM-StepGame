import itertools
import numpy as np
from functools import partial
# from tot.models import gpt
from tot.models import gpt as gpt

def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    print('get_value:######\n')
    # print('input x:', x)
    print('input y:\n', y)
    last_line = y.strip().split('\n')[-1]

    value_prompt = task.value_prompt_wrap(x, y)
    # print('value_prompt:',value_prompt)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    if 'Answer: '  in last_line:
        value_outputs = 'Arrive at answer'
    else:
        value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    print('value_outputs:', value_outputs)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    print('value:', value)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    print(values)
    return values

def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values

def get_proposals(task, x, y, n_generate_sample): 
    print('get_proposals:######\n')
    # print('input x:', x)
    # print('input y:\n', y)
    propose_prompt = task.propose_prompt_wrap(x, y)
    if y=='':
        proposals = gpt(propose_prompt, n=1, stop='\n\n')
    else:
        proposals = gpt(propose_prompt, n=n_generate_sample, stop='\n\n')
    print('proposals:',proposals)
    return [y + _ + '\n' for _ in proposals]
    # if y=='':
    #     return [y + _ + '\n' for _ in proposals]
    # elif 'answer' in proposals[0].lower():
    #     return [y + _ + '\n' for _ in proposals]
    # else:
    #     if len(proposals) > 0:
    #         return [y + _ + '\n' for _ in proposals]
    #     else:
    #         proposals = gpt(propose_prompt, n=n_generate_sample, stop=None)[0].split('\n')
    #         print('Regenerate proposals:',proposals)
    #         if len(proposals) > 1:
    #             return [y + _ + '\n' for _ in proposals[1:]]
    #         else: 
    #             return [y + _ + '\n' for _ in proposals]

def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    x = task.get_input(idx)  # input
    ys = ['']  # current output candidates
    infos = []
    # for step in range(task.steps):
    if args.method_generate == 'propose':
        ys = [get_proposals(task, x, y, args.n_generate_sample) for y in ys]
    ys = list(itertools.chain(*ys))
    stop = True
    while stop==True:
        # generation
        # if args.method_generate == 'sample':
        #     new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
        if args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y, args.n_generate_sample) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        # elif args.method_select == 'drop':
        #     select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
            # select_ids = sorted([x for x in ids if values[x] > 0.1], key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        if all(values[x] == 0 for x in select_ids):
            select_new_ys = [new_ys[select_id] for select_id in select_ids]
            stop = False
        if any(values[x] == 200 for x in select_ids):
            select_ids = sorted([x for x in ids if values[x] == 100], key=lambda x: values[x], reverse=True)[:args.n_select_sample]
            select_new_ys = [new_ys[select_id] for select_id in select_ids]
            stop = False
        else:
            select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        # infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        infos.append({'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, {'steps': infos}

def naive_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
    return ys, {}
import os
import pickle
import time
from clingo.control import Control
from clingo.symbol import parse_term
import pandas as pd
import openai
import requests


API_KEY = ''  # Enter your GPT-3 API key here
ORG_KEY = ''

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
        # GPT-3
        ###########
        self.org_key = ORG_KEY
        self.api_key = API_KEY
        self.engine = 'text-davinci-003'
        self.temperature = 0
        self.max_tokens = 1500
        self.prompt = {} # a mapping from prompt kind (str) to the prompt (str)
        self.count = 0 # a counter for the number of GPT-3 query
        ###########
        # Cache
        ###########
        self.path_cache = {} # store the mapping from kind (str) to cache file (str)
        self.cache = {} # store the GPT3 responses for visited stories
        self.path_mistakes = 'mistakes.xlsx' # file to store the wrong pridictions
        self.mistakes = [] # store the wrong predictions

        for k,v in args.items():
            setattr(self, k, v)
        # init openai account
        if self.org_key:
            openai.organization = self.org_key
        openai.api_key = self.api_key

    def load_prompt(self, kind_to_path):
        for kind in kind_to_path:
            with open(kind_to_path[kind], 'r', encoding='utf-8') as f:
                self.prompt[kind] = f.read()

    def load_cache(self):
        for kind in self.path_cache:
            if os.path.isfile(self.path_cache[kind]):
                with open(self.path_cache[kind], 'rb') as f:
                    self.cache[kind] = pickle.load(f)
            else:
                self.cache[kind] = {}
    
    def save_cache(self):
        for kind in self.path_cache:
            with open(self.path_cache[kind], 'wb') as f:
                pickle.dump(self.cache[kind], f, protocol=pickle.HIGHEST_PROTOCOL)

    # take a sentence and its kind, return the GPT3 response
    def gen_response(self, sentence, kind):
        # generate and cache the response in cache if it's not cached before
        if sentence not in self.cache[kind]:
            # print('==== Call GPT-3 ====')
            self.count += 1
            # print out the counting for every 100 queries
            if self.count % 100 == 0:
                print(self.count)
            # time.sleep(2)
            try:
                self.cache[kind][sentence] = openai.Completion.create(
                    prompt=self.prompt[kind] + sentence.strip() + '\nSemantic Parse:',
                    engine=self.engine,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens)
                self.save_cache()
            except Exception as e:
                print(e)
                self.cache[kind][sentence] = None

        # obtain the response from cache
        response = ''
        if self.cache[kind][sentence] is not None:
            response = self.cache[kind][sentence]['choices'][0]['text'].strip()
        # stop if response is empty due to content filtering or other issue
        assert response != '', 'Error: GPT-3 response is empty'
        # print('response:',response)
        return response
    
    # take a list of GPT3 responses and return the answer set
    def gen_answer_set(self, responses, opt=False):
        """
        Args:
            responses (str): a string of ASP facts
            opt (bool): if true, only optimal answer sets are returned
                        leave it to False when there is no weak constraint
        """
        program = self.asp_program + responses
        clingo_control = Control(['0', '--warn=none', '--opt-mode=optN', '-t', '4'])
        models = []
        try:
            clingo_control.add('base', [], program)
            clingo_control.ground([('base', [])], context=Context())
        except:
            if self.debug:
                print(responses)
                breakpoint()
            return []
        if opt:
            clingo_control.solve(on_model = lambda model: models.append(model.symbols(atoms=True)) if model.optimality_proven else None)
        else:
            clingo_control.solve(on_model = lambda model: models.append(model.symbols(atoms=True)))
        models = [[str(atom) for atom in model] for model in models]
        # print(models)
        return models

    # return the answer sets for an example data instance
    def eval_single_example(self, example, facts='', clean=False, opt=False):
        """
        Args:
            example (dict): a mapping from kind (str) to a list of sentences
            facts (str): additionally facts used during inference
            clean (bool): if true, remove all quotes turn all letters into lower case
        """
        response = ''
        for kind in example:
            for sentence in example[kind]:
                response += self.gen_response(sentence, kind)
        if clean:
            response = response.replace('\"', '').lower()
        # any dash between words should be replaced by underscore in clingo
        response = response.replace('-', '_')  ##here responses are parsed relations
        # print('response:',response)
        # print("facts",facts)
        answer_sets = self.gen_answer_set(response + '\n\n' + facts, opt=opt)
        # print(answer_sets)
        return answer_sets, response

    def save_mistakes(self, mistake_cols):
        df = pd.DataFrame(self.mistakes, columns=mistake_cols)
        df.to_excel(self.path_mistakes)


class Baseline(Pipeline):
    # take the name of a prompt context and an [INPUT], return the GPT3 response
    def gen_response(self, name, inp):
        # print(self.prompt[name].replace('[INPUT]', inp))

        # generate and cache the response if it's not cached before
        if inp not in self.cache[name] or self.cache[name][inp] == None:
            time.sleep(3)
            if self.engine.find("gpt-4") != -1:
                try:
                    self.api_key = ''
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.ChatCompletion.create(
                        engine=self.engine, #"gpt-4" "gpt-3.5-turbo"
                        messages=[
                        {"role": "user", "content": "%s"%(self.prompt[name].replace('[INPUT]', inp))}
                        ],                       
                        temperature = self.temperature,
                        max_tokens = self.max_tokens,
                        # top_p = 0.5,
                        stop = ["\n\nStory:"],
                        )                   
                    self.save_cache()
                    # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            elif self.engine.find("turbo") != -1:
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.ChatCompletion.create(
                      engine=self.engine,
                      messages = [{"role":"user","content": "%s"%(self.prompt[name].replace('[INPUT]', inp))}],
                      temperature=0,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],)
                    self.save_cache()
                      # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            
            elif self.engine.find("claude") != -1:
                try:
                      url = ""            
                      headers = {
                      }     
                      
                      data = {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": self.prompt[name].replace('[INPUT]', inp),
                                }
                            ],
                            "model": "claude-2",
                            "temperature":self.temperature,
                            "max_tokens_to_sample": self.max_tokens,
                            "stop_sequences": "\n\nStory:",
                      }
                      res = requests.post(url, headers=headers, json=data)
                      print("res.json()",res.json())
                      time.sleep(30)
                      self.cache[name][inp] = res.json()
                      self.save_cache()   
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            
            else: # GPT-3
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.Completion.create(
                      engine=self.engine,
                      prompt=self.prompt[name].replace('[INPUT]', inp),
                      temperature=self.temperature,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],
                      )
                    self.save_cache()
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None    

                
                
        # obtain the response from cache
        response = ''
        # if self.cache[name][inp]
        # print("self.cache[name][inp]",type(self.cache[name][inp]['choices'][0]['text'].strip()))
        if self.cache[name][inp] is not None:
            
            if self.engine.find("gpt-4") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            elif self.engine.find("turbo") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            elif self.engine.find("claude") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']    
            else:
                # response = self.cache[name][inp]['choices'][0]['text'].strip()
                response = self.cache[name][inp]['choices'][0]['text']
        # stop if response is empty due to content filtering or other issue
        # print(response)
        assert response != '', 'Error: GPT-3 response is empty'
        return response

    # return the answer sets for an example data instance
    def eval_single_example(self, example):
        """
        Args:
            example (dict): a mapping from prompt name (str) to an input example (str)
        """
        response = {}
        for name in example:
            # print(name)   #base
            if name in self.prompt:
                response[name] = self.gen_response(name, example[name])
        return response

class ToTCoTline(Pipeline):
    # take the name of a prompt context and an [INPUT], return the GPT3 response
    def gen_response(self, name, inp, chain):
        # print(self.prompt[name].replace('[INPUT]', inp))

        # generate and cache the response if it's not cached before
        self.count += 1
        # print out the counting for every 100 queries
        # if inp not in self.cache[name]:
            # print(self.cache[name])
            # print('no, not in')
        if self.count % 200 == 0:
            print(self.count)
            
        # if inp not in self.cache[name]:
        if inp not in self.cache[name] or self.cache[name][inp] == None:

            # print(inp)
            # time.sleep(3)
            # print('==== Call GPT-3 ====')
            if self.engine.find("gpt-4") != -1:
                try:
                    self.api_key = ''
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.ChatCompletion.create(
                        engine=self.engine, #"gpt-4" "gpt-3.5-turbo"
                        messages=[
                        {"role": "user", "content": "%s"%(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))}
                        ],                       
                        temperature = self.temperature,
                        max_tokens = self.max_tokens,
                        # top_p = 0.5,
                        stop = ["\n\nStory:"],
                        )                   
                    self.save_cache()
                    # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            elif self.engine.find("turbo") != -1:
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    # print('prompt: ####\n\n')
                    # print(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))
                    self.cache[name][inp] = openai.ChatCompletion.create(
                      engine=self.engine,
                      messages = [{"role":"user","content": "%s"%(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))}],
                      temperature=0,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],)
                    self.save_cache()
                      # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            else:
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.Completion.create(
                      engine=self.engine,
                      prompt=self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain),
                      temperature=self.temperature,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],
                      )
                    self.save_cache()
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None    
                
                
        # obtain the response from cache
        response = ''
        # if self.cache[name][inp]
        # print("self.cache[name][inp]",type(self.cache[name][inp]['choices'][0]['text'].strip()))
        if self.cache[name][inp] is not None:
            
            if self.engine.find("gpt-4") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            elif self.engine.find("turbo") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            else:
                # response = self.cache[name][inp]['choices'][0]['text'].strip()
                response = self.cache[name][inp]['choices'][0]['text']
        # stop if response is empty due to content filtering or other issue
        # print(response)
        assert response != '', 'Error: GPT-3 response is empty'
        return response

    # return the answer sets for an example data instance
    def eval_single_example(self, example, chain):
        """
        Args:
            example (dict): a mapping from prompt name (str) to an input example (str)
        """
        response = {}
        for name in example:
            # print(name)   #base
            if name in self.prompt:
                response[name] = self.gen_response(name, example[name], chain)
        return response

class ToTCoTline(Pipeline):
    # take the name of a prompt context and an [INPUT], return the GPT3 response
    def gen_response(self, name, inp, chain):
        # print(self.prompt[name].replace('[INPUT]', inp))

        # generate and cache the response if it's not cached before
        self.count += 1
        # print out the counting for every 100 queries
        # if inp not in self.cache[name]:
            # print(self.cache[name])
            # print('no, not in')
        if self.count % 200 == 0:
            print(self.count)
            
        # if inp not in self.cache[name]:
        if inp not in self.cache[name] or self.cache[name][inp] == None:

            # print(inp)
            # time.sleep(3)
            # print('==== Call GPT-3 ====')
            if self.engine.find("gpt-4") != -1:
                try:
                    self.api_key = ''
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.ChatCompletion.create(
                        engine=self.engine, #"gpt-4" "gpt-3.5-turbo"
                        messages=[
                        {"role": "user", "content": "%s"%(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))}
                        ],                       
                        temperature = self.temperature,
                        max_tokens = self.max_tokens,
                        # top_p = 0.5,
                        stop = ["\n\nStory:"],
                        )                   
                    self.save_cache()
                    # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            elif self.engine.find("turbo") != -1:
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    # print('prompt: ####\n\n')
                    # print(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))
                    self.cache[name][inp] = openai.ChatCompletion.create(
                      engine=self.engine,
                      messages = [{"role":"user","content": "%s"%(self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain))}],
                      temperature=0,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],)
                    self.save_cache()
                      # print(self.cache[name][inp]['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None
            else:
                try:
                    openai.api_type = ""
                    openai.api_base = ""
                    openai.api_version = ""
                    self.cache[name][inp] = openai.Completion.create(
                      engine=self.engine,
                      prompt=self.prompt[name].replace('[INPUT]', inp).replace('[Chain]', chain),
                      temperature=self.temperature,
                      max_tokens=self.max_tokens,
                      # top_p=0.5,
                      # frequency_penalty=0,
                      # presence_penalty=0,
                      stop=["\n\nStory:"],
                      )
                    self.save_cache()
                except Exception as e:
                    print(e)
                    self.cache[name][inp] = None    
                
                
        # obtain the response from cache
        response = ''
        # if self.cache[name][inp]
        # print("self.cache[name][inp]",type(self.cache[name][inp]['choices'][0]['text'].strip()))
        if self.cache[name][inp] is not None:
            
            if self.engine.find("gpt-4") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            elif self.engine.find("turbo") != -1:
                response = self.cache[name][inp]['choices'][0]['message']['content']
            else:
                # response = self.cache[name][inp]['choices'][0]['text'].strip()
                response = self.cache[name][inp]['choices'][0]['text']
        # stop if response is empty due to content filtering or other issue
        # print(response)
        assert response != '', 'Error: GPT-3 response is empty'
        return response

    # return the answer sets for an example data instance
    def eval_single_example(self, example, chain):
        """
        Args:
            example (dict): a mapping from prompt name (str) to an input example (str)
        """
        response = {}
        for name in example:
            # print(name)   #base
            if name in self.prompt:
                response[name] = self.gen_response(name, example[name], chain)
        return response

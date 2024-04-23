# SpatialLM-StepGame
This repository contains code and data related to the AAAI-24 paper [Advancing Spatial Reasoning in Large Language Models: An In-depth Evaluation and Enhancement Using the StepGame Benchmark](https://arxiv.org/abs/2401.03991).




## Installation
To get started, you can install the required packages using pip:

```shell
pip install openai==0.27.8 clingo==5.6 tqdm
```

## Data

The StepGame dataset utilized in this repository follows the bAbI format and is sourced from the [StepGame repository](https://github.com/ZhengxiangShi/StepGame/tree/main/Code/babi_format/). The data folder 'data/clean' and 'data/noise' contains all files from the StepGame repository's clean and noise data.

### Corrected Benchmark:
To obtain the 'correct_clean' and 'correct_noise' data samples (by removing examples that contain sentences using incorrect templates), you can run the following Python script:

```shell
python correct.py
```

## Solution for the Corrected Benchmark
To run solutions for the corrected benchmark, execute the following Python script:
```shell
python asp_solution.py
```

### Sentence-to-Relation Mapping:
For a detailed list of sentence-to-relation mappings, please refer to the Python file named 'sentence_to_relation.py' within this repository.

### Logical reasoning with ASP:
We utilize the ASP reasoning module 'location', which incorporates rules for spatial reasoning in a 2D grid space. This module is introduced by the [LLM-ASP repository](https://github.com/azreasoners/LLM-ASP).


## Evaluation
To obtain the results shown in Figure 4, run the following Python script:
```shell
python baseline.py
```
When executing baseline.py for evaluation, you can use the following arguments:

--num: This argument is optional and has a default value of 100. It specifies the maximum number of data items to be evaluated per file.

--engine: This argument is optional and has a default value of "gpt-35-turbo". It allows you to specify the engine name for evaluation, which can be one of the following options: "gpt-35-turbo" or "text-davinci-003". Note that cached evaluation results are available for these engines.

--prompt_type: This argument is optional and has a default value of 'base'. It allows you to set the type of prompts for evaluation. You can choose from two options: 'base' or 'base_clean1_3_5_7_10.'

By adjusting these arguments when running baseline.py, you can control the evaluation process as needed.

Within the directory named cached_responses/evaluation, you'll find cached responses of the LLLM stored in pickle files, along with records of mistakes in an XLSX file.

### Exploring Additional Evaluation Settings:
To evaluate under different settings without cached data, you'll need to configure the pipeline_base.py file. Please make the necessary adjustments in the pipeline.py file by providing your OpenAI or Claude API and configuring the following lines:
```python
API_KEY = ''  API_KEY = ''  # Enter your GPT-3 API key here

self.api_key = ''
openai.api_type = ""
openai.api_base = ""
openai.api_version = ""

url = ""            
headers = {}   
```

### 5-shot Separate Prompting
Please make the necessary configurations in the pipeline.py file before proceeding to execute the following Python script.
```shell
python separate_prompt.py --prompt_type base_5shot --kstart 1 --kend 11 
```
Within the directory named cached_responses/5shot_seperate, you'll find cached responses of the LLLM stored in pickle files, along with records of mistakes in an XLSX file.

## Our CoT and ToT Prompting

### CoT
```shell
python separate_prompt.py --prompt_type our_CoT_5shot --kstart 2 --kend 11 
```
--path_mistakes: This argument is to set the path to store mistakes file.

### ToT

```shell
python ToT_CoT.py --prompt_type our_CoT_5shot --kstart 3 --kend 11 
```
--path_mistakes: This argument is to set the path to store mistakes file.

Within the directory named cached_responses/correct_clean/ToT_logs, you'll find cached ToT generation data related to ToT reasoning chain-building process. For this particular set of experiments, we conducted experiments on 20 examples for each value of 'k'.

If you wish to execute the reasoning chain-building process on additional examples, please follow these steps:

1. Our ToT implementation is based on the [tree-of-thought-llm repository](https://github.com/princeton-nlp/tree-of-thought-llm). To get started, please refer to the instructions provided in the linked repository for the installation of 'tree-of-thought-llm'.

2. Setting up the StepGame task:

Set up the new task class: place 'SpatialLM-StepGame/ToT/src/tot/stepgame.py' and 'SpatialLM-StepGame/ToT/src/tot/__init__.py' into the directory '/tree-of-thought-llm/src/tot/tasks/'

Set up task-specific bfs: place 'SpatialLM-StepGame/ToT/src/tot/bfs.py' in the directory '/tree-of-thought-llm/src/tot/methods/'.

Set up task-specific prompts: place 'SpatialLM-StepGame/ToT/src/prompts/stepgame.py' in the directory '/tree-of-thought-llm/src/tot/prompts/'. 

Data: Copy all data files  in 'SpatialLM-StepGame/data/correct_clean/' to '/tree-of-thought-llm/src/tot/data/stepgame/correct_clean/'

(FYI: need to set the API Key in the file  /tree-of-thought-llm/src/tot/models.py)

3. place 'SpatialLM-StepGame/ToT/run_stepgame.oy' in the directory '/tree-of-thought-llm/' and execute it using the following command: 
```shell

![Visual Abstract of Paper](https://github.com/Fangjun-Li/SpatialLM-StepGame/blob/main/poster.jpg)
python run_stepgame.py
```
--task: For our StepGame task, this argument specifies the configuration of the input data file in the format 'stepgame_k', where 'k' represents the number of hops. (The default value is 'stepgame_3').
--task_start_index: Determines the starting point for the examples (default is 0).
--task_end_index: Indicates the endpoint for the examples (default is 20).

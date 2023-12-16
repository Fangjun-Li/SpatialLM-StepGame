# SpatialLM-StepGame
This repository contains code and data related to the AAAI-24 paper "Advancing Spatial Reasoning in Large Language Models: An In-depth Evaluation and Enhancement Using the StepGame Benchmark."

## Installation
To get started, you can install the required packages using pip:

```shell
pip install openai==0.27.8 clingo==5.6 tqdm
```

## Data

The StepGame dataset utilized in this repository follows the bAbI format and is sourced from the [StepGame repository](https://github.com/ZhengxiangShi/StepGame/tree/main/Code/babi_format/). The data folder 'data/clean' and 'data/noise' contains all files from the StepGame repository's clean and noise data.

#### Corrected Benchmark:
To obtain the 'correct_clean' and 'correct_noise' data samples (by removing examples that contain sentences using incorrect templates), you can run the following Python script:

```python
python correct.py
```

## Solution for the Corrected Benchmark
To run solutions for the corrected benchmark, execute the following Python script:
```python
python asp_solution.py
```

#### Sentence-to-Relation Mapping:
For a detailed list of sentence-to-relation mappings, please refer to the Python file named 'sentence_to_relation.py' within this repository.

#### Logical reasoning with ASP:
We utilize the ASP reasoning module 'location,' which incorporates rules for spatial reasoning in a 2D grid space. This module is introduced by the [LLM-ASP repository](https://github.com/azreasoners/LLM-ASP).


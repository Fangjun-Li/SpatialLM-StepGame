# SpatialLM-StepGame
Codes and data for AAAI-24 paper "Advancing Spatial Reasoning in Large Language Models: An In-depth Evaluation and Enhancement Using the StepGame Benchmark"

## Installation
```
pip install openai clingo==5.6 tqdm
```

## Data
The StepGame dataset presented here is the bAbI format, sourced from the [StepGame repository](https://github.com/ZhengxiangShi/StepGame/tree/main/Code/babi_format/). The data folder 'data/clean' and 'data/noise' contains all files from the StepGame repository's clean and noise data.

### Corrected Benchmark:
To obtain the correct_clean and correct_noise data samples (by removing examples that contain sentences using incorrect templates):
```python
python correct.py
```

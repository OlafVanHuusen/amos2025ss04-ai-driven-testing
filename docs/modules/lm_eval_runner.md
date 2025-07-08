## Model Evaluation with lm_eval

### Overview

This module benchmarks your local or Hugging Face-hosted models using the lm-evaluation-harness on the HumanEval task.

### How to Run

```bash
python backend/main.py --modules lm_eval_runner
```

This will:
- Execute the HumanEval test suite
- Automatically save the result to `outputs/human_eval/`
- Print the pass@1 score to the console

### Model Selection

Edit the model that gets evaluated inside `LmEvalRunner` (`modules/lm_eval_runner.py`).

Example using a CPU-based Hugging Face model:
```python
"--model_args", "pretrained=microsoft/phi-1_5,device=cpu"
```

### CUDA Support

For GPU acceleration, change:
```
device=cpu
```
to:
```
device=cuda
```

### Parameters

- `--model hf`: Use Hugging Face model backend
- `--model_args`: Passes model config: `pretrained=<HF_ID>,device=cpu/cuda`
- `--tasks humaneval`: Run only the HumanEval task
- `--limit 1`: Limits evaluation to 1 sample (for testing only)
- `--batch_size 1`: Evaluation batch size
- `--output_path`: Where to store the output .json file
- `--confirm_run_unsafe_code`: Required for HumanEval
- `--command-order`: Execute modules in the sequence given in terminal

### Output

Results are saved to:
```
outputs/human_eval/result_<timestamp>.json
```

### Known Issues

- Large models can freeze or crash if run on CPU
- Script may hang if the model is too large for system memory
- May require Hugging Face login: `huggingface-cli login`
- Some models may require manual access grant on huggingface.co

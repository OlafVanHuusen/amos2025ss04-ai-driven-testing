## Context Size Calculator Module

### Overview

The Context Size Calculator counts tokens in prompts against model context limits to prevent errors. It ensures that the combined token count of user prompts and system messages doesn't exceed the model's maximum context window.

### Features

- Uses model-specific Hugging Face tokenizers for precise token counting
- Includes both user prompts and system messages in calculations
- Provides fallback estimation when tokenizers are unavailable
- Caches tokenizers locally to reduce dependency on Hugging Face Hub

### Fallback Algorithm

When tokenizers fail, the module uses:
- Multiple heuristics (character, word, and space-based)
- Returns the highest estimate to prevent false negatives

### Usage

The module automatically integrates into the prompt processing pipeline when activated. It:

1. **Requires metadata** from `prompt_data`:
   - `model`: Model name/ID for tokenizer selection
   - `ollama_parameters/prompt`: User prompt text to analyze
   - `ollama_parameters/system`: System message text to include in count
   - `ollama_parameters/options/num_ctx`: Max token number as set in the ollama settings

2. **Adds metadata** to `prompt_data`:
   - `token_count`: Total token count
   - `token_count_estimated`: Boolean indicating if count was estimated

### Adding New Model Tokenizers

1. **Find the Model on Hugging Face**: Visit [huggingface.co](https://huggingface.co) and locate your target model
2. **Verify Open Source License**: Ensure the model has an open-source license that includes tokenizer access
3. **Update Model Mapping**: Add the Hugging Face model ID to the `_get_huggingface_model_id()` method in `context_size_calculator.py`:
   ```python
   model_mapping = {
       # ...existing mappings...
       "your-ollama-model:tag": "huggingface-org/model-name",
   }
   ```
4. **Automatic Download**: Run the program with the Context Size Calculator module enabled
5. **Handle Gated Models** (if needed): Some models require Hugging Face authentication

> **Note:** If tokenizer download fails, the module will fall back to estimation algorithms.
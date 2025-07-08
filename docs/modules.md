## Modules

This project supports a flexible **module interface** that lets you plug in custom functionality before and after the prompt is sent to the LLM.

---

### ✅ How to Use

Add the `--modules` flag when using the CLI:

```bash
python main.py --model 0 --modules example_logger
```

You can pass multiple modules seperated by spaces:

```bash
python main.py --model 0 --modules example_logger execute_tests calculate_ccc
```

---

### Available Modules

**Pre**-execution means the module acts before the prompt to the LLM, likely analyzing the input.

**Post**-execution means the module works after the prompt to the LLM, ergo on the output.


| Module | Description | Pre | Post | Additional Information |
|--------|-------------|:---:|:----:|------------------------|
| `calculate_ccc` | Calculates Cognitive Code Complexity (CCC) for code | ✅ | ✅ | Quantifies cognitive effort needed to understand code.  |
| `calculate_mcc` | Calculates McCabe Cyclomatic Complexity for Python code | ✅ | ✅ | Measures complexity based on number of independent execution paths in code. Uses AST analysis and requires valid Python syntax. |
| `clean_output_code` | Automatically fixes and repairs generated test code | ❌ | ✅ | Runs multiple iterations providing the LLM with syntax and runtime error information. |
| `context_size_calculator` | Checks prompt size against model context limits | ✅ | ❌ | Prevents token limit overflows before sending to the model. Uses the models tokenizers when available or falls back to heuristic estimation. |
| `example_logger` | Simple logging module for demonstrating the usage of modules | ✅ | ✅ | |
| `execute_tests` | Executes generated code (typically unit tests) | ❌ | ✅ | Runs Python code in a controlled environment and captures results. Uses Docker for isolated execution with proper error handling. |
| `include_project` | RAG module that includes a GitHub project context | ✅ | ❌ | Clones repositories and provides relevant code context to the model. Uses vector embeddings for semantic retrieval of similar code snippets. |
| `internet_search` | Performs DuckDuckGo searches to augment prompts | ✅ | ❌ | Extracts keywords from user queries to find relevant information online. Enriches prompts with web content to improve model responses. |
| `lm_eval_runner` | Runs HumanEval benchmarks with LM-eval framework | ❌ | ✅ | Evaluates model performance on standardized coding tasks. Stores output files in outputs/human_eval. |
| `metrics_collector` | Collects and stores performance metrics | ❌ | ✅ | Records syntax validity, loading times, and generation times. Stores results as JSON files in both latest and archived outputs directories. |
| `prune_duplicate_tests` | Removes duplicate test functions and assertions | ❌ | ✅ | Improves quality of generated test code by eliminating redundancy. Uses code similarity detection to identify and remove duplicates. |
| `show_control_flow` | Visualizes code as control flow graphs | ✅ | ✅ | Generates SVG diagrams showing execution paths and decision points. Stores the visualisation files under outputs/control_flow. |
| `text_converter` | Extracts and cleans Python code from responses | ✅ | ✅ | Extracts code blocks from markdown responses and formats them with Black. Core module that saves processed code to files for other modules to use. |
| `timeout` | Sets a default timeout for LLM requests | ✅ | ❌ | Prevents hanging on slow or non-responsive model queries. Default value is 30 seconds but can be adjusted as needed.

---

### 🧱 Module Structure

Each module must:
- Live in the `modules/` folder
- Inherit from `ModuleBase`
- Be named using `snake_case.py`
- Contain a class with the `CamelCase` equivalent of the filename

Example (shortened):

**modules/calculate_ccc.py**

```python
class CalculateCcc(ModuleBase):
    """Berechnet die Cognitive Code Complexity (CCC) für Quell- und Ausgabecode."""

    preprocessing_order = 5
    postprocessing_order = 5

    def __init__(self):
        super().__init__()

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return [TextConverter]

    def process_prompt(self, prompt_data: dict) -> dict:
        ...processing_prompt...

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        ...processing_response...

```

---

### ⚙️ Base Module Interface

**modules/base.py**

```python
from abc import ABC, abstractmethod
from schemas import PromptData, ResponseData


class ModuleBase(ABC):
    @abstractmethod
    def applies_before(self) -> bool:
        """Return True if the module runs before prompt is sent."""
        pass

    @abstractmethod
    def applies_after(self) -> bool:
        """Return True if the module runs after response is received."""
        pass

    def dependencies(self) -> list[type["ModuleBase"]]:
        """
        Return a list of other ModuleBase subclasses this module depends on.
        Default is empty.
        """
        return []

    def dependencies_names(self) -> list[str]:
        """
        Return a list of names of other ModuleBase subclasses this module depends on.
        Default is empty.
        """
        return [dep.__name__ for dep in self.dependencies()]

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        """Optionally modify the prompt."""
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """Optionally modify or analyze the response."""
        return response_data

```

---

### 🧩 Adding New Modules

1. Create a file in `modules/` (e.g., `my_module.py`)
2. Add a class `MyModule` that inherits from `ModuleBase`
3. Return `True` from `applies_before()` and/or `applies_after()`
4. Implement `process_prompt()` and/or `process_response()`
5. Add a pre- or postprocessing order number to have it run before or after other modules
6. Add a list of modules your module is dependent on
7. Run your script using:

```bash
python main.py --modules my_module
```

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



## [🧪 Example Usage of each module](#-example-usage-of-each-module)

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

### 🧪 Example Usage of each module

#### Source Code
```python
def bubble_sort(arr):
    """Sort a list using the bubble sort algorithm.

    This implementation includes an optimization that stops the algorithm
    when no swaps are needed, indicating that the list is already sorted.

    Args:
        arr: The list to be sorted (modified in-place)

    Returns:
        None: The input list is modified in-place
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
```

#### User Message
Create unit tests for the given python code

#### Basic Execution
**Command:** `python main.py --model 4 (qwen3)`

#### Basic Response

Here are some unit tests for the `bubble_sort` function using Python's `unittest` framework:

```python
import unittest

def bubble_sort(arr):
    """Sort a list using the bubble sort algorithm.

    This implementation includes an optimization that stops the algorithm
    when no swaps are needed, indicating that the list is already sorted.

    Args:
        arr: The list to be sorted (modified in-place)

    Returns:
        None: The input list is modified in-place
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break

class TestBubbleSort(unittest.TestCase):
    def test_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_already_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, using the bubble sort algorithm.

    def test_with_duplicates(self):
        arr = [3, 2, 1, 2, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 3, 3])

    def test_empty_list(self):
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_list(self):
        arr = [5]
        bubble_sort(arr)
        self.assertEqual(arr, [5])

if __name__ == '__main__':
    unittest.main()
```

#### Explanation:
- The `TestBubbleSort` class contains several test cases:
  - `test_sorted_list`: Tests a list that is already sorted.
  - `test_unsorted_list`: Tests a list that needs to be fully sorted.
  - `test_already_sorted_list`: Tests a list that is already sorted (should not perform any swaps).
  - `test_with_duplicates`: Tests a list with duplicate elements.
  - `test_empty_list`: Tests an empty list.
  - `test_single_element_list`: Tests a list with a single element.

To run these tests, simply execute the script.

---

## Module Results

### `text_converter`
*Note: This module is now included in all cases since it's such a basic module*

**Command:** `python main.py --model 4 --module text_converter`

```python
import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest

import unittest

def bubble_sort(arr):
    pass

    """Sort a list using the bubble sort algorithm.

    This implementation includes an optimization that stops the algorithm
    when no swaps are needed, indicating that the list is already sorted.

    Args:
        arr: The list to be sorted (modified in-place)

    Returns:
        None: The input list is modified in-place
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break

class TestBubbleSort(unittest.TestCase):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, using the bubble sort algorithm.

        arr = [3, 2, 1, 2, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 3, 3])

        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

        arr = [5]
        bubble_sort(arr)
        self.assertEqual(arr, [5])

if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    unittest.main()
```

**Result:** Syntax Error in the third assert of TestBubbleSort

### `clean_output_code`
*Note: This module will be used alongside other modules that require working code*

**Command:** `python main.py --model 4 --module clean_output_code`

```python
import sys
from pathlib import Path

sys.path.insert(0, "/code/extracted")  # Add extracted dir to import path
from prompt import bubble_sort

import unittest


class TestBubbleSort(unittest.TestCase):
    def test_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reversed_list(self):
        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_already_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_with_duplicates(self):
        arr = [3, 2, 1, 2, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 3, 3])

    def test_empty_list(self):
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_list(self):
        arr = [5]
        bubble_sort(arr)
        self.assertEqual(arr, [5])


if __name__ == "__main__":
    unittest.main()
```

**Result:** Runs all tests without errors

### `calculate_ccc`

**Command:** `python main.py --model 4 --module clean_output_code calculate_ccc`

```
[CalculateCCC] Using Python CCC calculator for source code
[CalculateCCC] Calculated CCC: 293
...
[CalculateCCC] Python CCC calculator failed: Code not recognized as valid Python code. 
[CalculateCCC] Using general CCC estimator for source code
[CalculateCCC] Calculated CCC: 368
```

### `calculate_mcc`

**Command:** `python main.py --model 4 --module clean_output_code calculate_mcc`

```
[CalculateMCC] Calculated input MCC: 5
[CalculateMCC] Calculated output MCC: 8
```


### `context_size_calculator`

**Command:** `python main.py --model 4 --module context_size_calculator`

```
[ContextSizeCalculator] Counting tokens for model: qwen3:4b-q4_K_M
[ContextSizeCalculator] Loading tokenizer from local cache: /home/user/amos_version_3/amos2025ss04-ai-driven-testing-1/backend/modules/context_size_calculator_lib/tokenizers/Qwen_Qwen3-4B
[ContextSizeCalculator] Token count: 169
```

### `execute_tests`

**Command:** `python main.py --model 4 --module execute_tests`

```json
{
  "exit_code": 1,
  "stdout": "",
  "stderr": "  File \"/code/response.py\", line 44\n    self.assertEqual(arr, [1, 2, using the bubble sort algorithm.\n                                 ^^^^^^^^^\nSyntaxError: invalid syntax. Perhaps you forgot a comma?\n",
  "status": "failure"
}
```

### `include_project`
**Additional resource provided:** https://gist.github.com/aprilmintacpineda/81a571a40500982015a8ae87947298d8 (repo with code and tests for BubbleSort)

**Command:** `python main.py --model 4 --module include_project text_converter`

```python
import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest

import unittest

class TestBubbleSort(unittest.TestCase):
        arr = [1, 2, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3])
        arr = [3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3])
        arr = [1, 2, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3])
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])
        arr = [5]
        bubble_sort(arr)
        self.assertEqual(arr, [5])

if __name__ == "__main__":
    unittest.main()
```

**Result:** Simpler Test, but working right out of the box

### `internet_search`

**Basic command:** `python main.py --model 4 --module text_converter internet_search`

```python
def bubble_sort(arr):
    """Sort a list using the bubble sort algorithm.

    This implementation includes an optimization that stops the algorithm
    when no swaps are needed, indicating that the list is already sorted.

    Args:
        arr: The list to be sorted (modified in-place)

    Returns:
        None: The input list is modified in-place
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
```

**Result:** Prompt + Internet search results are too big for the default context window, resulting in the LLM returning the source_code as the answer.


**Adjusted command:** `python main.py --model 4 --module text_converter internet_search context_size_calculator --num_ctx 7000`
*(Setting context windows to 7000 and testing wether the context window is still too small)*

```python
import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest

import unittest


class TestBubbleSort(unittest.TestCase):
    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reversed_array(self):
        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        arr = [5, 1, 4, 2, 8]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 4, 5, 8])

    def test_empty_array(self):
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_array(self):
        arr = [42]
        bubble_sort(arr)
        self.assertEqual(arr, [42])

    def test_array_with_duplicates(self):
        arr = [3, 2, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 3])


if __name__ == "__main__":
    unittest.main()
```

**Result:** Perfect result

### `lm_eval_runner`
*Note: Not really a module, more like a standalone benchmark for LLMs, hence not examplified here*

### `metrics_collector`

**Command:** `python main.py --model 4 --module metrics_collector`

```json
{
  "Model": "Qwen3",
  "Syntax Valid": false,
  "Loading Time (s)": 30.2,
  "Generation Time (s)": 30.2
}
```

### `prune_duplicate_tests`

**Command:** `python main.py --model 4 --module clean_output_code prune_duplicate_tests`

```
Pruning duplicate tests and asserts:
Original number of tests found: 6
After pruning duplicates: 6 tests remaining

Original number of assert statements: 6
After pruning duplicates: 4 assert statements remaining
```

*Note: Deleted two asserts wrongly according to log, didn't delete anything in the end actually*

### `show_control_flow`
**Command:** `python main.py --model 4 --module clean_output_code show_control_flow`

would store an image like ![image cant be loaded](https://py2cfg.readthedocs.io/en/latest/_static/fib_cfg.svg)
in `outputs/control_flow`

### `timeout`

**Command:** `python main.py --model 4 --module timeout`

*Note: Timeout set to 1 second for demonstration purpose here*

```
/home/olaf_van_huusen/amos_version_3/amos2025ss04-ai-driven-testing-1/backend/llm_manager.py:203: UserWarning: Timeout reached after 1 seconds. 
  warnings.warn(f"Timeout reached after {request_timeout} seconds. ")
```
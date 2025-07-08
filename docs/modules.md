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

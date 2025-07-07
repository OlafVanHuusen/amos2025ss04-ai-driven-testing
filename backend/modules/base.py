from abc import ABC, abstractmethod
from schemas import PromptData, ResponseData


class ModuleBase(ABC):
    """
    Abstract base class for all processing modules in the LLM execution pipeline.

    Modules can hook into two stages of the prompt-response lifecycle:
    - Before the prompt is sent to the language model
    - After the response is received from the model

    Subclasses can:
    - Define whether they apply before and/or after LLM execution.
    - Modify or enrich the prompt (`process_prompt`).
    - Analyze or transform the model response (`process_response`).
    - Declare dependencies on other modules to enforce execution order.

    Usage:
        All custom modules must inherit from this class and implement at least
        `applies_before()` and/or `applies_after()`.

    Default behavior (optional overrides):
        - `dependencies()`: declare other modules that must run before this one.
        - `process_prompt()`: modify or inspect the prompt before it's sent.
        - `process_response()`: modify or inspect the model's response after it's received.

    Returns:
        Modified `PromptData` and/or `ResponseData` objects as appropriate.
    """

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

from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class ExampleLogger(ModuleBase):
    """
    Logging module that prints prompt inputs and model responses to the console.

    This module is primarily intended for debugging and transparency during development.
    It logs the content of the prompt before sending it to the model and the output
    returned by the model after inference.
    """

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return []

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        print("[ExampleLogger] Prompt being sent:")
        print(prompt_data.input)
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        print("[ExampleLogger] Response received:")
        print(response_data.output)
        return response_data

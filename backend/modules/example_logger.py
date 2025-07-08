from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class ExampleLogger(ModuleBase):
    """
    Logging-Modul, das die Eingabeaufforderungen (Prompts) und Modellantworten in der Konsole ausgibt.

    Dieses Modul dient hauptsächlich der Fehlersuche und Transparenz während der Entwicklung.
    Es protokolliert den Inhalt des Prompts, bevor er an das Modell gesendet wird, sowie die Ausgabe,
    die nach der Inferenz vom Modell zurückgegeben wird.
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

from abc import ABC, abstractmethod
from schemas import PromptData, ResponseData


class ModuleBase(ABC):
    """
    Abstrakte Basisklasse für alle Verarbeitungsmodule in der Ausführungspipeline eines LLMs (Large Language Models).

    Module können sich in zwei Phasen des Prompt-Antwort-Zyklus einklinken:
    - Bevor der Prompt an das Sprachmodell gesendet wird
    - Nachdem die Antwort vom Modell empfangen wurde

    Unterklassen können:
    - Festlegen, ob sie vor und/oder nach der Ausführung des LLMs angewendet werden.
    - Den Prompt verändern oder erweitern (`process_prompt`).
    - Die Antwort des Modells analysieren oder transformieren (`process_response`).
    - Abhängigkeiten zu anderen Modulen deklarieren, um die Ausführungsreihenfolge sicherzustellen.

    Verwendung:
        Alle benutzerdefinierten Module müssen von dieser Klasse erben und mindestens
        `applies_before()` und/oder `applies_after()` implementieren.

    Standardverhalten (kann überschrieben werden):
        - `dependencies()`: Gibt andere Module an, die vor diesem Modul ausgeführt werden müssen.
        - `process_prompt()`: Modifiziert oder inspiziert den Prompt vor dem Absenden.
        - `process_response()`: Modifiziert oder inspiziert die Modellantwort nach dem Empfang.

    Rückgabe:
        Angepasste `PromptData`- und/oder `ResponseData`-Objekte, je nach Phase.
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

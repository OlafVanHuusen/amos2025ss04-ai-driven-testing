from modules.base import ModuleBase
import warnings
from modules.calculate_ccc_lib.ccc_calculator_python import (
    get_ccc_for_code as get_ccc_for_code_python,
)
from modules.calculate_ccc_lib.ccc_estimator_general import (
    get_ccc_for_code as get_ccc_for_code_general,
)
from modules.text_converter import TextConverter

# Error handling in this module is a mess, but it works 👍


class CalculateCcc(ModuleBase):
    """
    Modul zur Berechnung der Cognitive Code Complexity (CCC) für Quell- und Ausgabecode.

    Diese Klasse ist in eine Verarbeitungspipeline integriert und berechnet automatisch
    die kognitive Komplexität von Code, der im Prompt (Eingabe) oder als Antwort (Ausgabe)
    vom Modell generiert wurde. CCC ist ein Metrik, die den kognitiven Aufwand quantifiziert,
    der zum Verstehen eines Codes nötig ist.
    """

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
        source_code = prompt_data.input.source_code
        if not source_code:
            warnings.warn(
                "[CalculateCCC] No source code found in prompt_data.input.source_code. Cannot calculate CCC. "
            )
            return prompt_data

        try:
            ccc = get_ccc_for_code_python(source_code)
            print("[CalculateCCC] Using Python CCC calculator for source code")
        except Exception as e:
            print(f"[CalculateCCC] Python CCC calculator failed: {e}")
            ccc = get_ccc_for_code_general(source_code)
            print("[CalculateCCC] Using general CCC estimator for source code")

        if ccc is None:
            warnings.warn(
                f"[CalculateCCC] Could not calculate CCC for source code {source_code}. "
                "See warnings for more details."
            )
        else:
            print(f"[CalculateCCC] Calculated CCC: {ccc}")

        prompt_data.ccc_complexity = ccc

        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        output_code = response_data.output.code
        if not output_code:
            warnings.warn(
                "[CalculateCCC] No code found to be extracted from response.Cannot calculate CCC. Debug the text_converter module for further information. "
            )
            return response_data

        try:
            ccc = get_ccc_for_code_python(output_code)
            print("[CalculateCCC] Using Python CCC calculator for source code")
        except Exception as e:
            print(f"[CalculateCCC] Python CCC calculator failed: {e}")
            ccc = get_ccc_for_code_general(output_code)
            print("[CalculateCCC] Using general CCC estimator for source code")

        if ccc is None:
            warnings.warn(
                f"[CalculateCCC] Could not calculate CCC for code {output_code}. "
                "See warnings for more details."
            )
        else:
            print(f"[CalculateCCC] Calculated CCC: {ccc}")

        response_data.output.ccc_complexity = ccc

        return response_data

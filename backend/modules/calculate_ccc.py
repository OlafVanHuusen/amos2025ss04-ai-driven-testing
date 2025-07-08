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
    Module for calculating the Cognitive Code Complexity (CCC) of both source and output code.

    This class integrates into a processing pipeline to automatically evaluate the complexity
    of code provided in a prompt (input) and the generated response (output). CCC is a metric
    that aims to quantify the cognitive effort required to understand a piece of code.

    Key Features:
    - Calculates CCC before and after model inference (both prompt and response).
    - Uses a Python-specific CCC calculator when possible, and falls back to a general estimator if needed.
    - Adds the resulting CCC value to the respective data dictionary (`prompt_data` or `response_data`).
    - Issues warnings if source or output code is missing or if the CCC calculation fails.
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

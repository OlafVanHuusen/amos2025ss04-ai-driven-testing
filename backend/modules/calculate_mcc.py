from .base import ModuleBase
from mccabe import PathGraphingAstVisitor
import os
from schemas import PromptData, ResponseData
import sys
import ast
from modules.text_converter import TextConverter


class CalculateMcc(ModuleBase):
    """
    Module for calculating the McCabe Cyclomatic Complexity (MCC) of Python code using AST analysis.

    This module analyzes both the input (prompt) and output (response) Python code to determine
    their cyclomatic complexity—a measure of code complexity based on the number of independent
    paths through the source code. The complexity is computed using abstract syntax tree (AST) traversal.

    Features:
    - Executes both before and after model inference.
    - Extracts code either from file paths (if available) or directly from data fields.
    - Uses AST-based analysis to calculate total MCC via `get_code_complexity_sum`.
    - Handles and logs exceptions during parsing or complexity calculation.
    - Stores the MCC value in `prompt_data.mcc_complexity` and `response_data.output.mcc_complexity`.
    """

    preprocessing_order = 5
    postprocessing_order = 5

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return [TextConverter]

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        prompt_path = prompt_data.prompt_code_path
        if prompt_path and os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = prompt_data.input.source_code

        try:
            mcc = get_code_complexity_sum(prompt, filename="stdin")
            print("[CalculateMCC] Calculated MCC:", mcc)
        except Exception as e:
            print(f"[CalculateMCC] Could not calculate MCC for prompt: {e}")
            mcc = None

        prompt_data.mcc_complexity = mcc
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        response_path = response_data.output.output_code_path
        if response_path and os.path.exists(response_path):
            with open(response_path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            code = getattr(response_data.output, "code", None) or getattr(
                response_data.output, "markdown", ""
            )

        try:
            mcc = get_code_complexity_sum(code, filename="stdin")
            print("[CalculateMCC] Calculated MCC:", mcc)
        except Exception as e:
            print(f"[CalculateMCC] Could not calculate MCC for response: {e}")
            mcc = None

        response_data.output.mcc_complexity = mcc
        return response_data


def get_code_complexity_sum(code, filename="stdin"):
    try:
        tree = compile(code, filename, "exec", ast.PyCF_ONLY_AST)
    except SyntaxError:
        e = sys.exc_info()[1]
        sys.stderr.write(
            "[CalculateMCC] Unable to parse %s: %s\n" % (filename, e)
        )
        return 0

    visitor = PathGraphingAstVisitor()
    visitor.preorder(tree, visitor)
    total_complexity = 0
    for graph in visitor.graphs.values():
        total_complexity += graph.complexity()
    return total_complexity

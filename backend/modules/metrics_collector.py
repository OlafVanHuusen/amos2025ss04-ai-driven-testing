import json
from pathlib import Path
from datetime import datetime
from modules.base import ModuleBase
from schemas import PromptData, ResponseData
from modules.text_converter import TextConverter


class MetricsCollector(ModuleBase):
    """
    Sammelt und speichert Leistungsmetriken, nachdem die Modellantwort generiert wurde.

    Dieses Modul wird nach Abschluss aller anderen Verarbeitungsschritte ausgeführt. Es misst und speichert:
      - Die syntaktische Gültigkeit des generierten Codes (über einen `compile()`-Check in Python)
      - Die Ladezeit und Generierungszeit während der Modellausführung
      - Metadaten des verwendeten Modells (z. B. Modellname)

    Die Metriken werden als 'metrics.json' sowohl im Verzeichnis 'outputs/latest/' als auch in einem
    zeitgestempelten Archiv unter 'outputs/archive/' gespeichert.

    Abhängigkeiten:
        - Erfordert, dass das TextConverter-Modul zuvor ausgeführt wurde, um sicherzustellen, dass der generierte Code verfügbar ist.

    Rückgabewert:
        Aktualisiertes `ResponseData`-Objekt mit gesetztem 'syntax_valid'-Flag.
    """

    def __init__(self):
        self.loading_time = None
        self.generation_time = None
        self.latest_dir = None
        self.archive_dir = None

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return [TextConverter]

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        # Prepare folders
        model_name = prompt_data.model.name
        output_code_path = Path(response_data.output.output_code_path)

        # Skip re-saving and check directly
        syntax_valid = self.check_syntax_validity(output_code_path)
        # Save cleaned code
        self.latest_dir, self.archive_dir = self.make_output_dirs(model_name)
        response_data.output.syntax_valid = syntax_valid

        metrics = {
            "Model": model_name,
            "Syntax Valid": syntax_valid,
            "Loading Time (s)": round(response_data.timing.loading_time, 2),
            "Generation Time (s)": round(
                response_data.timing.generation_time, 2
            ),
        }

        self.write_to_outputs("metrics.json", json.dumps(metrics, indent=4))

        return response_data

    def make_output_dirs(self, model_name):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        archive_dir = (
            Path("outputs/archive")
            / f"{timestamp}_{model_name.lower().replace(' ', '_')}"
        )
        latest_dir = Path("outputs/latest")

        archive_dir.mkdir(parents=True, exist_ok=True)
        latest_dir.mkdir(parents=True, exist_ok=True)

        return latest_dir, archive_dir

    def write_to_outputs(self, filename, content: str):
        for directory in [self.latest_dir, self.archive_dir]:
            path = directory / filename
            if filename.endswith(".json"):
                path.write_text(content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    @staticmethod
    def check_syntax_validity(file_path):
        try:
            with open(file_path, "r") as f:
                code = f.read()
            compile(code, str(file_path), "exec")
            return True
        except SyntaxError as e:
            print(f"[MetricsCollector] Syntax Error: {e}")
            return False

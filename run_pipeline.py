import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.api_request import main as fetch_api_data


def to_pascal_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def run_pipeline() -> None:
    print("Fetching FHIR resources from the API...")
    fetch_api_data()

    print("API fetch complete. Running extractors...")

    extract_dir = ROOT / "app" / "extract"
    for module_file in sorted(extract_dir.glob("*.py")):
        if module_file.name == "__init__.py":
            continue

        module_name = module_file.stem
        module_path = extract_dir / module_file.name
        if not module_path.exists():
            continue

        try:
            module = importlib.import_module(f"app.extract.{module_name}")
        except Exception as exc:
            print(f"Skipping {module_name}: import failed ({exc})")
            continue

        extractor = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if attr_name.startswith("extract_") and callable(attr):
                extractor = attr
                break

        if extractor is None:
            continue

        source_filename = f"{to_pascal_case(module_name)}_data.json"
        source_path = ROOT / "app" / source_filename
        if not source_path.exists():
            print(f"Skipping {module_name}: expected {source_filename} was not generated.")
            continue

        print(f"Running {module_name} -> {source_filename}")
        try:
            extractor(source_filename)
            output_file = f"{module_name}.json"
            output_path = ROOT / "app" / output_file
            if output_path.exists():
                print(f"Created {output_file}")
            else:
                print(f"Finished {module_name}, but {output_file} was not created.")
        except Exception as exc:
            print(f"Extractor {module_name} failed: {exc}")


if __name__ == "__main__":
    run_pipeline()
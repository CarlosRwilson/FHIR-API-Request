import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields 
from app.functions import get_resource, extract_nested_display

def extract_medication(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    medications = []
    
    for item in entry:

        common = extract_common_fields(item)
        resource = get_resource(item)

        code = resource.get('code', {})
        code_id = extract_nested_display(code)
        text = code.get('text', '')

        contained = extract_nested_display(resource.get('contained', []))
        form = extract_nested_display(resource.get('form', {}))

        medication_dict = {
            **common,
            'Medicine': code_id,
            'text': text,
            'Contained': contained,
            'Form': form

        }

        medications.append(medication_dict)
    save_json(medications, 'medication.json')
if __name__ == '__main__':
    extract_medication('Medication_data.json')
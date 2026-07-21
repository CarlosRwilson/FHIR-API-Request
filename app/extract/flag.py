import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource

def extract_flag(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    flags = []

    for items in entry:
        
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue

        category = first_or_empty(resource.get('category', []))
        category_val = extract_nested_display(category) or category.get('text', '')

        code = resource.get('code', {})
        code_val = extract_nested_display(code) or code.get('text', '')

        subject = resource.get('subject', {})
        patient = subject.get('reference', '') or subject.get('display', '')

        flag_dict = {
            **common,
            'Category': category_val,
            'Code': code_val,
            'Patient': patient
        }

        flags.append(flag_dict)
    save_json(flags, 'flag.json')


if __name__ == '__main__':
    extract_flag('Flag_data.json')
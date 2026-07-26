import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, extract_nested_display, extract_personal_info
from app.functions import first_or_empty, extract_display

def extract_related_person(json_file: str) -> None:
    data = open_file(json_file)
    entry = data.get('entry', [])
    related_people = []

    for item in entry:
        resource = item.get('resource', {})

        if not resource:
            continue

        common = extract_common_fields(item)
        personal_info = extract_personal_info(item)

        relationship = extract_nested_display(resource.get('relationship', [])) 
        

        patient = extract_display(resource.get('patient', {})) 
    

        related_person_dict = {
            **common,
            **personal_info,
            'Active': resource.get('active', ''),
            'Patient': patient,
            'Relationship': relationship,
        }

        related_people.append(related_person_dict)

    save_json(related_people, 'related_person.json')


if __name__ == '__main__':
    extract_related_person('RelatedPerson_data.json')
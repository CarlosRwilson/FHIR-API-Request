import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource

def extract_healthcare_service(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    healthcare_data = []

    for items in entry:
    
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue

        extension = extract_nested_display(resource.get('extension', []))
        active = resource.get('active', '')

        name = resource.get('name', '')
        characteristic = extract_nested_display(resource.get('characteristic', []))

        provided_by = resource.get('providedBy', {})
        provided_reference = provided_by.get('reference', '')

        location = first_or_empty(resource.get('location', []))
        location_reference = location.get('reference', '')

        type = extract_nested_display(resource.get('type', []))

        healthcare = {
            **common,
            'Extension': extension,
            'Active': active,
            'Name': name,
            'Characteristic': characteristic,
            'Provided By': provided_reference,
            'Location': location_reference,
            'Type': type
        }

        healthcare_data.append(healthcare)

    save_json(healthcare_data, 'healthcare_service.json')
    
if __name__ == '__main__':
    extract_healthcare_service('HealthcareService_data.json')
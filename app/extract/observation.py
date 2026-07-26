import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, extract_nested_display, extract_reference_range
from app.functions import save_json, get_resource, extract_common_fields, extract_display

def extract_observation(json_file: str) -> None:
 
    data = open_file(json_file)
 
    entry = data.get('entry', [])
 
    observations = []
 
    for item in entry:

        resource = get_resource(item)
        common = extract_common_fields(item)
 
        if not resource:
            continue

        category = extract_nested_display(resource.get('category', []))
        code = extract_nested_display(resource.get('code', {}))

        patient = extract_display(resource.get('subject', {}))

        effective_date_time = resource.get('effectiveDatetime', '')
 
        value_quantity = resource.get('valueQuantity', {})
        reference_range = extract_reference_range(resource.get('referenceRange', []))

        observation_dict = {
            **common,
            'Category': category,
            'Code': code,
            'Patient': patient,
            'Effective Datetime': effective_date_time,
            'Value Quantity': value_quantity,
            **reference_range
        }

        observations.append(observation_dict)
    
    save_json(observations, 'observation.json')

if __name__ == '__main__':
    extract_observation('Observation_data.json')
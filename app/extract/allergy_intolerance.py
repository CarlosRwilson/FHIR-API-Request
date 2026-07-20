import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] 
sys.path.insert(0, str(ROOT))

from app.functions import first_or_empty, open_file, extract_nested_display
from app.functions import save_json, get_resource, extract_common_fields

def extract_allergies(json_file: str) -> None:
    
    data = open_file(json_file)
    
    entry = data.get('entry', [])
    
    allergies = []
    
    for item in entry:

        resource = get_resource(item)
        common = extract_common_fields(item)
        
        if not resource:
            continue

        reference = resource.get('patient', {})
        patient = reference.get('reference', '')

        recorder = resource.get('recorder', {})
        practitioner = recorder.get('reference', '')

        allergy = extract_nested_display(resource.get('code', {}))
        category = first_or_empty(resource.get('category', []))

        reaction = extract_nested_display(resource.get('reaction', []))
        
        """
        ** -> Dictionary unpacking operator
              takes all the key-value pairs from 
              one dictionary and inserts them into another dictionary.
        """
        
        allergie_info = {
            **common,
            'Patient': patient,
            'Practitioner': practitioner,
            'Allergy': allergy,
            'Reaction': reaction ,
            'Category': category
            }
        
        allergies.append(allergie_info)

    save_json(allergies, 'allergie_intolerance.json')

if __name__ == '__main__':
    extract_allergies('AllergyIntolerance_data.json')
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] 
sys.path.insert(0, str(ROOT))

from app.functions import first_or_empty, open_file, extract_display, save_json

def extract_allergies(json_file: str) -> None:
    
    data = open_file(json_file)
    
    entry = data.get('entry', [])
    
    allergies = []
    
    for item in entry:

        full_url = item.get('fullUrl', '') 
        resource = item.get('resource',{})
        
        if not resource:
            continue

        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '') 
        
        reference = resource.get('patient', {})
        patient = reference.get('reference', '')

        recorder = resource.get('recorder', {})
        practitioner = recorder.get('reference', '')

        code = resource.get('code', {})
        first_coding = first_or_empty(code.get('coding', []))
        allergy = first_coding.get('display', '') 

        category = first_or_empty(resource.get('category', []))

        reaction = extract_display(resource.get('reaction', []))

        personal_info = {
            'ID': resource.get('id', ''),
            'FullUrl': full_url,
            'Patient': patient,
            'Practitioner': practitioner,
            'Allergy': allergy,
            'Reaction': reaction ,
            'Category': category,
            'Last Updated': last_updated
        }
        allergies.append(personal_info)
    save_json(allergies, 'allergie_intolerance.json')
if __name__ == '__main__':
    extract_allergies('AllergyIntolerance_data.json')
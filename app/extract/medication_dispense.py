import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields 
from app.functions import get_resource, extract_nested_display, extract_display

def extract_medication_dispense(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    medications_dispense = []
    
    for item in entry:

        common = extract_common_fields(item)
        resource = get_resource(item)

        medication_codeable = extract_nested_display(resource.get('medicationCodeableConcept', {}))
        patient = extract_display(resource.get('subject', {}))

        quantity = resource.get('quantity', {})
        days_supply = resource.get('daysSupply', {})
        time_supply = days_supply.get('value', '')

        handed_over = resource.get('whenHandedOver', '')

        dispense_dict = {
            **common,
            'Medication Concept': medication_codeable,
            'Patient': patient,
            'Quantity': quantity,
            'Days Supply': f'{time_supply} days',
            'Handed Over': handed_over

        }

        medications_dispense.append(dispense_dict)
   
    save_json(medications_dispense, 'medication_dispense.json')

if __name__ == '__main__':
    extract_medication_dispense('MedicationDispense_data.json')
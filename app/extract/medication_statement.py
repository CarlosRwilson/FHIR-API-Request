import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty 
from app.functions import get_resource, extract_nested_display, extract_display

def extract_medication_dispense(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    medications_statement = []
    
    for item in entry:

        common = extract_common_fields(item)
        resource = get_resource(item)

        medication_codeable = extract_nested_display(resource.get('medicationCodeableConcept', {}))

        patient = extract_display(resource.get('subject', {}))

        reason_code = extract_nested_display(resource.get('reasonCode', []))

        contained = extract_nested_display(resource.get('contained', []))
        dosage = first_or_empty(resource.get('dosage', []))
        text = dosage.get('text', '')

        dispense_dict = {
            **common,
            'Medication': medication_codeable or contained,
            'Patient': patient,
            'Reason Code': reason_code,
            'Dosage': text

        }

        medications_statement.append(dispense_dict)
    save_json(medications_statement, 'medication_statement.json')

if __name__ == '__main__':
    extract_medication_dispense('MedicationStatement_data.json')
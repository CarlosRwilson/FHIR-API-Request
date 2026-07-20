import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource

def extract_condition(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    condition_data = []

    for items in entry:
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue

        clinical_status = extract_nested_display(resource.get('clinicalStatus', {}))

        verification_status = extract_nested_display(resource.get('verificationStatus', {}))
        
        category = first_or_empty(resource.get('category', []))

        disease = resource.get('code', {})
        
        subject = resource.get('subject', {})
        patient = subject.get('reference', '')

        on_set_date_time = resource.get('onsetDateTime', '') 
        abatement_date_time = resource.get('abatementDateTime', '')
        recorded_date = resource.get('recordedDate', '')

        asserter = resource.get('asserter', {})
        practitioner = asserter.get('reference', '')

        note = first_or_empty(resource.get('note', []))
        
        condition_info = {
            **common,
            'Clinical Status': clinical_status,
            'Verification Status': verification_status,
            'Category': category,
            'Disease': disease,
            'Patient': patient,
            'On set DateTime': on_set_date_time,
            'Abatement DateTime': abatement_date_time,
            'Recorder Date': recorded_date,
            'Practitioner': practitioner,
            'Note': note
        }
        condition_data.append(condition_info)
    save_json(condition_data, 'condition.json')

if __name__ == '__main__':
    extract_condition('Condition_data.json')
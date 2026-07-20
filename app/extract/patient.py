import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, extract_personal_info

def extract_pacients(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])
    patients = []
    
    for item in entry:

        common = extract_common_fields(item)
        patient_info = extract_personal_info(item)

        personal_info = {
            **common, 
            **patient_info
        }

        patients.append(personal_info)

    save_json(patients, 'patient.json')

if __name__ == '__main__':
    extract_pacients('Patient_data.json')
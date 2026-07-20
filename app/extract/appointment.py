from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_nested_display 
from app.functions import extract_participants, get_resource, extract_common_fields

def extract_appointment(json_file: str) -> None:
    
    data = open_file(json_file)

    entry = data.get('entry', [])

    appointment_data = []

    for item in entry:
       
        resource = get_resource(item)
        common = extract_common_fields(item)
        
        if not resource:
            continue

        participants = extract_participants(resource.get('participant', []))

        service_type = extract_nested_display(resource.get('serviceType', []))

        appointment_info = {
            **common,
            'Participants': participants,
            'Service Type': service_type,
        }

        appointment_data.append(appointment_info)
    
    save_json(appointment_data, 'appointment.json')

if __name__ == '__main__':
    extract_appointment('Appointment_data.json')
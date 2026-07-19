from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, first_or_empty, extract_display, extract_participants

def extract_appointment(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    appointment_data = []


    for item in entry:
        full_url = item.get('fullUrl', '')
        resource = item.get('resource', {})
        if not resource:
            continue
        
        id = resource.get('id', '')

        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '')
        status = resource.get('status', '')

        participants = extract_participants(resource.get('participant', []))

        service_type = extract_display(resource.get('serviceType', []))

        appointment_info = {
            'FullUrl': full_url,
            'ID': id,
            'Last Updated': last_updated,
            'Status': status,
            'Participants': participants,
            'Service Type': service_type,
        }
        appointment_data.append(appointment_info)
    save_json(appointment_data, 'appointment.json')

if __name__ == '__main__':
    extract_appointment('Appointment_data.json')
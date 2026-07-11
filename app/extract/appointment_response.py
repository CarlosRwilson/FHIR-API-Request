import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import first_or_empty, open_file, save_json

def extract_appointment_response(json_file:str) -> None:

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

        identifier = resource.get('identifier', [])
        first_identifier = first_or_empty(identifier)
        identifier_val = first_identifier.get('value', '')

        appointment = resource.get('appointment', {})
        appointment_val = appointment.get('reference', '')

        actor = resource.get('actor', {})
        patient = actor.get('reference', '')

        participant_status = resource.get('participantStatus', '')
        comment = resource.get('comment', '')

        appointment_response = {
            'FullUrl': full_url,
            "ID": id, 
            'Identifier': identifier_val, 
            'Appointment': appointment_val,
            'Patient': patient,
            'Paticipant Status': participant_status,
            'Comment': comment

        }
        appointment_data.append(appointment_response)
    save_json(appointment_data, 'appointment_response.json')

if __name__ == '__main__':
    extract_appointment_response('AppointmentResponse_data.json')
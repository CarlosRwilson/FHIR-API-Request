import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json
from app.functions import extract_common_fields, get_resource

def extract_appointment_response(json_file:str) -> None:

    data = open_file(json_file)

    entry = data.get('entry', [])

    appointment_data = []

    for item in entry:
       
       resource = get_resource(item)
       common = extract_common_fields(item)

       if not resource:
           continue
     
       appointment = resource.get('appointment', {})
       appointment_val = appointment.get('reference', '')
       
       actor = resource.get('actor', {})
       patient = actor.get('reference', '')

       participant_status = resource.get('participantStatus', '')
       comment = resource.get('comment', '')   
       
       appointment_response_dict = {
           **common,
            'Appointment': appointment_val,
            'Patient': patient,
            'Paticipant Status': participant_status,
            'Comment': comment   
        }
       
       appointment_data.append(appointment_response_dict)
    
    save_json(appointment_data, 'appointment_response.json')

if __name__ == '__main__':
    extract_appointment_response('AppointmentResponse_data.json')
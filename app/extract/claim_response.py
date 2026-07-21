import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource, extract_display

def extract_claim_response(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    responses = []

    for items in entry:
        resource = get_resource(items)
        common = extract_common_fields(items)

        type = extract_nested_display(resource.get('type',{}))
        use = resource.get('use', '')

        created = resource.get('created', '')

        patient = extract_display(resource.get('patient', {}))
        insurer = extract_display(resource.get('insurer', {}))
        requestor = extract_display(resource.get('requestor', {}))
        request = extract_display(resource.get('request', {}))

        outcome = resource.get('outcome', '')
        disposition = resource.get('disposition', '')

        period = resource.get('preAuthPeriod', {})

        item = resource.get('item', [])
        first_item = first_or_empty(item)
        adjudication = first_item.get('adjudication', [])

        process_note = resource.get('processNote', [])

        claim_response_dict = {
            **common,
            'Type': type,
            'use': use,
            'Created': created,
            'Patient': patient,
            'Insurer': insurer,
            'Requestor': requestor,
            'Request': request,
            'Outcome': outcome,
            'Disposition': disposition,
            'Period': period,
            'Adjudication': adjudication,
            'Process Note': process_note
        }

        responses.append(claim_response_dict)
    save_json(responses, 'claim_response.json')

if __name__ == '__main__':
    extract_claim_response('ClaimResponse_data.json')
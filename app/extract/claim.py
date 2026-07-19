import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_display, first_or_empty

def extract_claim(json_file: str) -> None:
    data = open_file(json_file)
    entry = data.get('entry', [])

    claim_data = []

    for item in entry:
        full_url = item.get('fullUrl', '')
        resource = item.get('resource', {})

        if not resource:
            continue
        id = resource.get('id', '')
        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '')

        status = resource.get('status', '')
        type = extract_display(resource.get('type', {}))

        use = resource.get('use', '')

        patient = resource.get('patient', {})
        insurer = resource.get('insurer', {})
        provider = resource.get('provider', {})

        priority = extract_display(resource.get('priority', {}))

        care_team = resource.get('careTeam', [])
        first_team = first_or_empty(care_team)
        practitioner = first_team.get('provider', {})

        role = extract_display(first_team.get('role', {}))

        diagnosis = extract_display(resource.get('diagnosis', []))

        item = resource.get('item', [])
        first_item = first_or_empty(item)
        
        category = extract_display(first_item.get('category', {}))
        product_or_service = extract_display(first_item.get('productOrService', {}))

        serviced_period = first_item.get('servicedPeriod', {})

        location_concept = first_item.get('locationCodeableConcept', {})
        location_display = extract_display(location_concept)

        net = first_item.get('net', {})

        claim = {
            'fullUrl': full_url,
            'ID': id,
            'Last Updated': last_updated,
            'Status': status,
            'Serviced Period': serviced_period,
            'Type':type,
            'Use':use,
            'Patient': patient,
            'Insurer': insurer,
            'Provider': provider,
            'Priority': priority,
            'Practitioner': practitioner,
            'Role': role,
            'Diagnosis': diagnosis,
            'Category': category,
            'Product Or Service': product_or_service,
            'Location Concept': location_display,
            'Net': net
        }
        claim_data.append(claim)
    save_json(claim_data, 'claim.json')
if __name__ == '__main__':
    print(extract_claim('Claim_data.json'))
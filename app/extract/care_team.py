import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_display, extract_participants, first_or_empty

def extract_care_team(json_file: str) -> None:
    data = open_file(json_file)
    entry = data.get('entry', [])

    care_team_data = []

    for item in entry:
        full_url = item.get('fullUrl', '')
        resource = item.get('resource', {})
        if not resource:
            continue
        
        id = resource.get('id', '')
        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '')

        status = resource.get('status', '')
        period = resource.get('period', {})
        participants = extract_participants(resource.get('participant', []))
        role = extract_display(resource.get('participant', []))

        reason_code = extract_display(resource.get('reasonCode', []))
        
        organization = resource.get('managingOrganization', [])
        first_organization = first_or_empty(organization)
        organization_display = first_organization.get('display', '') 

        care_team = {
            'fullUrl': full_url,
            'ID': id,
            'Last Updated': last_updated, 
            'Status': status,
            'Period': period,
            'Participants': participants,
            'Role': role,
            "Reason Code": reason_code,
            'Organization': organization_display
        }
        care_team_data.append(care_team)
    save_json(care_team_data, 'care_team.json')

if __name__ == '__main__':
    print(extract_care_team('CareTeam_data.json'))
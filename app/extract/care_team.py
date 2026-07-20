import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_nested_display, extract_participants
from app.functions import first_or_empty, extract_common_fields, get_resource

def extract_care_team(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    care_team_data = []

    for item in entry:
        
        resource = get_resource(item)
        common = extract_common_fields(item)
        
        if not resource:
            continue
        
        period = resource.get('period', {})
        participants = extract_participants(resource.get('participant', []))
        role = extract_nested_display(resource.get('participant', []))

        reason_code = extract_nested_display(resource.get('reasonCode', []))
        
        organization = resource.get('managingOrganization', [])
        first_organization = first_or_empty(organization)
        organization_display = first_organization.get('display', '') 

        care_team = {
            **common,
            'Period': period,
            'Participants': participants,
            'Role': role,
            "Reason Code": reason_code,
            'Organization': organization_display
        }

        care_team_data.append(care_team)
    
    save_json(care_team_data, 'care_team.json')

if __name__ == '__main__':
    extract_care_team('CareTeam_data.json')
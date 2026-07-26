import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, extract_nested_display, extract_location_info
from app.functions import save_json, get_resource, extract_common_fields

def extract_organization(json_file: str) -> None:
 
    data = open_file(json_file)
 
    entry = data.get('entry', [])
 
    organizations = []
 
    for item in entry:

        resource = get_resource(item)
        common = extract_common_fields(item)
        contact_info = extract_location_info(item)
        
        if not resource:
            continue

        active = resource.get('active', '')
        type = extract_nested_display(resource.get('type', []))

        organization_dict = {
            **common,
            **contact_info,
            'Active': active,
            'Type': type
        }

        organizations.append(organization_dict)
    save_json(organizations, 'organization.json')

if __name__ == '__main__':
    extract_organization('Organization_data.json')
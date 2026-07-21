import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields 
from app.functions import extract_location_info, get_resource

def extract_location(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    locations = []
    
    for item in entry:

        common = extract_common_fields(item)
        resource = get_resource(item)

        contact_info = extract_location_info(item)

        position = resource.get('position', {})
        
        managing_organization = resource.get('managingOrganization', {})
        organization_val = managing_organization.get('display', '')

        location_dict = {
            **common,
            **contact_info,
            'Position': position,
            'Managing Organization': organization_val,

        }

        locations.append(location_dict)

    save_json(locations, 'location.json')

if __name__ == '__main__':
    extract_location('Location_data.json')
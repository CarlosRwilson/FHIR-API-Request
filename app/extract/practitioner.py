import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import first_or_empty, open_file, save_json

def extract_practitioners(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])
    practitioners = []
    
    for item in entry:
        full_url = item.get('fullUrl', '') 
        resource = item.get('resource',{})

        if not resource:
            continue
        
        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '') 

        identifier = resource.get('identifier', [])
        first_identifier = first_or_empty(identifier)
        value = first_identifier.get('value', '') 

        names = resource.get('name', [])
        first_name = first_or_empty(names)
        given_name = first_name.get('given', []) 
        family_name = first_name.get('family', '') 

        adresses = resource.get('address', [])
        first_adress = first_or_empty(adresses)
        line = first_adress.get('line', [])
        city = first_adress.get('city', '')
        district = first_adress.get('district', '')
        country = first_adress.get('country', '')
        postal_code = first_adress.get('postalCode', '')
        state = first_adress.get('state', '')

        personal_info = {
            'ID': resource.get('id', ''),
            'FullUrl': full_url,
            'Identifier': value,
            'Name': given_name,
            'Last Name': family_name,
            'Gender': resource.get('gender', ''),
            'Line': line,
            'City': city,
            'District': district,
            'Postal Code': postal_code,
            'Country': country,
            'State': state,
            'Telecom': resource.get('telecom',[]),
            'Birthdate': resource.get('birthDate', ''),
            'Last Updated': last_updated

        }
        practitioners.append(personal_info)
    save_json(practitioners, 'practitioners.json')

if __name__ =='__main__':
    extract_practitioners('Practitioner_data.json')
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import first_or_empty, open_file, save_json

def extract_pacients(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])
    pacients = []
    
    for item in entry:
        full_url = item.get('fullUrl', '')
        resource = item.get('resource', {})

        if not resource:
            continue

        meta = resource.get('meta', {})
        last_updated = meta.get('lastUpdated', '')
        names = resource.get('name', [])
        first_name_dict = first_or_empty(names)

        family_name = first_name_dict.get('family', '')
        given_names = first_name_dict.get('given', [])

        adresses = resource.get('address', [])
        first_adress = first_or_empty(adresses)
        line = first_adress.get('line', [])
        city = first_adress.get('city', '')
        district = first_adress.get('district', '')
        postal_code = first_adress.get('postalCode', '')
        country = first_adress.get('country', '')
        state = first_adress.get('state', '')

        personal_info = {
            'ID': resource.get('id', ''),
            'FullUrl': full_url,
            'Name': given_names,
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
        pacients.append(personal_info)

    save_json(pacients, 'patients.json')
if __name__ == '__main__':    
    extract_pacients('Patient_data.json')
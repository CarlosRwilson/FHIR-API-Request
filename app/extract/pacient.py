import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.functions import open_file, save_json

def extract_pacients(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])
    pacients = []
    
    for item in entry:
        resource = item.get('resource', {})

        if not resource:
            continue
        names = resource.get('name', [])
        first_name_dict = names[0] if names else {}
        family_name = first_name_dict.get('family', '')
        given_names = first_name_dict.get('given', [])

        adresses = resource.get('address', [])
        first_adress = adresses[0] if adresses else {}
        city = first_adress.get('city', '')
        line = first_adress.get('line'[0], {})
        district = first_adress.get('district', '')
        postal_code = first_adress.get('postalCode', '')
        country = first_adress.get('country', '')
        state = first_adress.get('state', '')

        personal_info = {
            'ID': resource.get('id', ''),
            'FullUrl': resource.get('fullUrl', ''),
            'Name': given_names,
            'Last Name': family_name,
            'Gender': resource.get('gender', ''),
            'Line': line,
            'City': city,
            'District': district,
            'Postal Code': postal_code,
            'Country': country,
            'State': state,
            'Telecom': resource.get('telecom',[])

        }
        pacients.append(personal_info)

    save_json(pacients, 'Pacients.json')
    

extract_pacients('Patient_data.json')


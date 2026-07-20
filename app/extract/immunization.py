import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource

def extract_immunization(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    immunization_data = []

    for items in entry:
    
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue

        vaccine_code = extract_nested_display(resource.get('vaccineCode', {}))
        vaccine_text = resource.get('text', '')

        patient = resource.get('patient', {})

        occurrence_date_time = resource.get('occurrenceDateTime', '')
        recorded = resource.get('recorded', '')
        primary_source = resource.get('primarySource', '')
        lot_number = resource.get('lotNumber', '')
        expiration_date = resource.get('expirationDate', '')

        site = extract_nested_display(resource.get('site', {}))

        route = extract_nested_display(resource.get('route', {}))

        dose_quantity = resource.get('doseQuantity', {})
        dose_val = dose_quantity.get('value', '')

        protocol = first_or_empty(resource.get('protocolApplied', []))
        protocol_applied = protocol.get('series', '')

        immunization_info = {
            **common,
            'Vaccine Code': vaccine_text,
            'Patient': patient,
            'Ocurrence DateTime': occurrence_date_time,
            'Recorded': recorded,
            'Primary Source': primary_source,
            'Lot Number': lot_number,
            'Expiration Date': expiration_date,
            'Site': site,
            'Route': route,
            'Dose Quantity': dose_val,
            'Protocol Applied': protocol_applied

        }
        immunization_data.append(immunization_info)

    save_json(immunization_data, 'immunization.json')

if __name__ == '__main__':
    extract_immunization('Immunization_data.json')


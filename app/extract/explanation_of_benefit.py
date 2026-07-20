import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import get_resource, extract_nested_display

def extract_benefit(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    benefits = []

    for items in entry:
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue
        
        type = extract_nested_display(resource.get('type', []))
        use = resource.get('use', '')

        patient = resource.get('patient', {})
        created = resource.get('created', '')
        
        insurer = resource.get('insurer', {})
        provider = resource.get('provider', {})

        outcome = resource.get('outcome', '')
        insurance = resource.get('insurance', [])

        item = resource.get('item', [])
        first_item = first_or_empty(item)
        product_or_service = extract_nested_display(first_item)

        adjudication = first_item.get('adjudication', {})

        total = first_or_empty(resource.get('total', []))

        benefit_info = {
            **common,
            'Type': type,
            'use': use,
            'Created': created,
            'Patient': patient,
            'Insurer': insurer,
            'Provider': provider,
            'Outcome': outcome,
            'Insurance': insurance,
            'Product or Service': product_or_service,
            'Adjudication': adjudication,
            'Total': total
            
        }

        benefits.append(benefit_info)
    
    save_json(benefits, 'explanation_of_benefit.json')

if __name__ == '__main__':
    extract_benefit('ExplanationOfBenefit_data.json')
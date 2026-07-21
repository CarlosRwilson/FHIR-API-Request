import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_nested_display
from app.functions import get_resource, extract_common_fields

def extract_care_plan(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])

    care_plans = []

    for item in entry:
        
        resource = get_resource(item)
        common = extract_common_fields(item)
        
        if not resource:
            continue

        intent = resource.get('intent', '')
        title = resource.get('title', '')
        description = resource.get('description', '')

        subject = resource.get('subject', {})
        patient = subject.get('display', '') or subject.get('reference', '')
       
        period = resource.get('period', {})

        category = extract_nested_display(resource.get('category', []))

        care_plan_dict = {
            **common,
            'Period': period,
            'Intent': intent,
            "Title": title,
            'Description': description,
            'Patient': patient,
            'Category': category,
        }

        care_plans.append(care_plan_dict)

    save_json(care_plans, 'care_plan.json')

if __name__ == '__main__':
    extract_care_plan('CarePlan_data.json')    
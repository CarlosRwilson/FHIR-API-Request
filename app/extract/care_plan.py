import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import save_json, open_file, extract_display, extract_activity

def extract_care_plan(json_file: str) -> None:
    data = open_file(json_file)
    entry = data.get('entry', [])

    care_plans = []

    for item in entry:
        full_url = item.get('fullUrl', '')
        resource = item.get('resource', {})
        if not resource:
            continue
        id = resource.get('id', '')
        
        date = resource.get('meta', {})
        last_updated = date.get('lastUpdated', '')

        status = resource.get('status', '')
        intent = resource.get('intent', '')
        title = resource.get('title', '')
        description = resource.get('description', '')

        subject = resource.get('subject', {})
        patient = subject.get('display', '') or subject.get('reference', '')
       
        period = resource.get('period', {})

        category = extract_display(resource.get('category', []))
        activity = extract_activity(resource.get('activity', []))

        care_plan = {
            'fullUrl': full_url,
            'ID': id,
            'Last Updated': last_updated, 
            'Status': status,
            'Period': period,
            'Intent': intent,
            "Title": title,
            'Description': description,
            'Patient': patient,
            'Category': category,
            'Activity': activity
        }
        care_plans.append(care_plan)
    save_json(care_plans, 'care_plan.json')

if __name__ == '__main__':
    print(extract_care_plan('CarePlan_data.json'))    
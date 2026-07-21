import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, first_or_empty
from app.functions import extract_nested_display, get_resource

def extract_family_members(json_file: str) -> None:
    
    data = open_file(json_file)
    entry = data.get('entry', [])

    family_members = []

    for items in entry:
        resource = get_resource(items)
        common = extract_common_fields(items)

        if not resource:
            continue

        patient = resource.get('patient', {})
        date = resource.get('date', '')

        relationship = extract_nested_display(resource.get('relationship', {}))

        sex = extract_nested_display(resource.get('sex', {}))
        
        deceased_age = resource.get('deceasedAge', {})
        value = deceased_age.get('value', '')

        note = first_or_empty(resource.get('note', []))
        text = note.get('text', '')

        condition = resource.get('condition', [])
        first_condition = first_or_empty(condition)
        display = extract_nested_display(first_condition)
        onset_age = first_condition.get('onsetAge', {})
        age_value = onset_age.get('value', '')

        members_dict = {
            **common,
            'Patient': patient,
            'Date': date,
            'Relationship': relationship,
            'Sex': sex,
            'Deceased Age': value,
            'Note': text,
            'Condition': display,
            'Onset Age': age_value
        }

        family_members.append(members_dict)
        
    save_json(family_members,'family_member_history.json' )
if __name__ == '__main__':
    extract_family_members('FamilyMemberHistory_data.json')
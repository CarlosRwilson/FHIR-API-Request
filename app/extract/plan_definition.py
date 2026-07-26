import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields, extract_nested_display
from app.functions import first_or_empty


def extract_plan_definition(json_file: str) -> None:
    data = open_file(json_file)
    entry = data.get('entry', [])
    plan_definitions = []

    for item in entry:
        resource = item.get('resource', {})

        if not resource:
            continue

        common = extract_common_fields(item)
        action = first_or_empty(resource.get('action', [])) 

        plan_definition_dict = {
            **common,
            'Name': resource.get('name', ''),
            'Title': resource.get('title', ''),
            'Type': extract_nested_display(resource.get('type', {})),
            'Status': resource.get('status', ''),
            'Description': resource.get('description', ''),
            'Library': resource.get('library', []),
            'Action Title': action.get('title', ''),
            'Action Description': action.get('description', ''),
            'Action Trigger': action.get('trigger', []),
        }

        plan_definitions.append(plan_definition_dict)

    save_json(plan_definitions, 'plan_definition.json')


if __name__ == '__main__':
    extract_plan_definition('PlanDefinition_data.json')
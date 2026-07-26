import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.functions import open_file, save_json, extract_common_fields
from app.functions import extract_display, first_or_empty


def extract_schedule(json_file: str) -> None:

    data = open_file(json_file)
    entry = data.get('entry', [])
    schedules = []

    for item in entry:
        resource = item.get('resource', {})

        if not resource:
            continue

        common = extract_common_fields(item)
        actor = first_or_empty(resource.get('actor', []))
        patient = extract_display(actor)
        


        planning_horizon = resource.get('planningHorizon', {}) 

        schedule_dict = {
            **common,
            'Active': resource.get('active', ''),
            'Actor': patient,
            'Planning Horizon Start': planning_horizon.get('start', ''),
            'Planning Horizon End': planning_horizon.get('end', ''),
            'Comment': resource.get('comment', ''),
        }

        schedules.append(schedule_dict)

    save_json(schedules, 'schedule.json')


if __name__ == '__main__':
    extract_schedule('Schedule_data.json')
import json
import os
import sys
from pathlib import Path

"""
Reusable and general functions
...
"""

JSON_FOLDER = Path(__file__).resolve().parent


def open_file(json_file: str | Path) -> dict:
    complete_path = JSON_FOLDER / json_file
    
    """
    Returns
    path/folder/file.json

    """

    if not complete_path.exists():
        raise FileNotFoundError(f'No such file or directory: {complete_path}')

    with open(complete_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(data: dict | list, filename: str) -> None:
    output_path = os.path.join(os.path.dirname(__file__), filename)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def first_or_empty(items: dict | list) -> dict:
    return items[0] if items else {}

def extract_display(obj: dict | list) -> list[str]:

    displays = []

    if isinstance(obj, dict):
        """
        Found a coding list
        """
        if 'coding' in obj:
            for coding in obj['coding']:
                display = coding.get('display')
                if display:
                    displays.append(display)
        """
        Continue searching deeper
        """    
        for value in obj.values():
            displays.extend(extract_display(value))
    
    elif isinstance(obj, list):
        for item in obj:
            displays.extend(extract_display(item))
    
    return displays

def extract_participants(obj: list[dict]) -> list[str]:
    participants = []
    
    for participant in obj:
        actor = participant.get('actor',{})
        
        if isinstance(actor, dict):
            reference = actor.get('reference', '')
            if reference:
                participants.append(reference)

    return participants
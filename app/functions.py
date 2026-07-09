import json
from pathlib import Path
import os
"""
Functions to
Parse
Save, open files
Extraction
...
possible
extract_names(practitioner)

extract_identifiers(practitioner)

extract_telecom(practitioner)

extract_addresses(practitioner)

extract_qualifications(practitioner)
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

def save_json(data:dict | list, filename:str) -> None:
    output_path = os.path.join(os.path.dirname(__file__), filename)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
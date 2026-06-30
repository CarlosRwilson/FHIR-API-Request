import requests
import os
import json

BASE = "https://hapi.fhir.org/baseR4"

r = requests.get(f'{BASE}/Patient')
response_json = r.json()

print(json.dumps(response_json, indent=4))

output_path = os.path.join(os.path.dirname(__file__), 'Patients_data.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(response_json, f, indent=4)

file_size_bytes = os.path.getsize(output_path)
file_size_kb = file_size_bytes / 1024

print(f'file size: {file_size_kb:.2f} KB')
print(f'Saved response to {output_path}')




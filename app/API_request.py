import requests
import json
from playwright.sync_api import sync_playwright
from app.functions import save_json

def get_resource_names(BASE_URL:str) -> list[str]:
    
    """
    Returns:
        [
            "Observation",
            "Patient",
            "Encounter",
            .....
        ]
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.wait_for_selector('#pageButtons')
        buttons = page.locator('#pageButtons a.pageButton')

        # Extract and clean the text content
        # E.g, 'Observation 1334456' -> 'Observation'
        raw_names = buttons.all_inner_texts()
        pages_names = [name.split()[0] for name in raw_names
                        if name.strip()] 

        #Filter out generic buttons
        page_names = [n for n in pages_names 
                      if n not in('All', "System",'Endpoint')]
        browser.close()
        return page_names

def data_request(BASE_URL:str, resource:str) -> dict | None:
    """
    Downloads all Observation resources.

    Returns:
        dict
    """
    try:
     response = requests.get(f'{BASE_URL}/{resource}')
     response.raise_for_status()
     return response.json()
    except requests.RequestException as e:
        print('ERROR', e)
        return None
    
BASE_URL = "https://hapi.fhir.org/baseR4" 

def main():
    resources = get_resource_names(BASE_URL)
    for resource in resources:
        data = data_request(BASE_URL, resource)

        if data is not None:
            save_json(data, f'{resource}_data.json') 

if __name__ == '__main__':
    main()
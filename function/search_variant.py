# function/search_variant.py

import requests
import json
import os

def save_to_json(filename, data):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    if data not in existing_data:
        existing_data.append(data)
    
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

# search_variant 查詢variant資料
def search_variant(query):
    url = "http://www.ncbi.nlm.nih.gov/research/litvar2-api/variant/autocomplete"
    params = {"query": query}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        save_to_json('data/search_variant_results.json', data)
    else:
        print(f"Request failed with status code {response.status_code}")

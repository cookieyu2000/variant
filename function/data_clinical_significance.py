# function/data_clinical_significance.py

import json
import requests
from urllib.parse import quote
import os

# 定义一个函数用于保存数据到JSON文件
def save_to_json(filename, rsid, data):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    # 检查新数据是否已经存在
    if not any(entry['rsid'] == rsid for entry in existing_data):
        data['rsid'] = rsid
        existing_data.append(data)
    
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
    else:
        print("Data already exists in the file.")

# data_clinical_significance Variant的臨床意義
def data_clinical_significance(variant_id):
    encoded_variant_id = quote(f"litvar@{variant_id}##")
    url = f"https://www.ncbi.nlm.nih.gov/research/litvar2-api/variant/get/{encoded_variant_id}?format=json"
    
    print(f"Requesting URL: {url}")
    
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            save_to_json('data/data_clinical_significance_results.json', variant_id, data)
        except json.JSONDecodeError:
            print("Error decoding JSON response")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

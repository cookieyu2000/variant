# function/variant_articles.py

from Bio import Entrez
import json
import os
import requests
import xml.etree.ElementTree as ET

# 使用Entrez email 参数
Entrez.email = "s112321523@mail1.ncnu.edu.tw"

def save_to_json(filename, data):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    if data not in existing_data:
        existing_data.append(data)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

def search_variant_articles(variant):
    # 构建搜索查询
    query = f"{variant}[Title/Abstract]"
    
    # 搜索PubMed数据库中的文章
    search_handle = Entrez.esearch(db="pubmed", term=query, retmax=100)
    search_results = Entrez.read(search_handle)
    search_handle.close()
    
    pubmed_ids = search_results["IdList"]
    
    # 获取PMC ID
    pmc_ids = []
    for pubmed_id in pubmed_ids:
        fetch_handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pubmed_id)
        fetch_results = Entrez.read(fetch_handle)
        fetch_handle.close()
        
        for linksetdb in fetch_results[0]["LinkSetDb"]:
            for link in linksetdb["Link"]:
                pmc_ids.append(link["Id"])

    result = {
        "variant": variant,
        "pubmed_ids": pubmed_ids,
        "pmc_ids": pmc_ids
    }
    
    return result

def save_variant_articles(variant):
    result = search_variant_articles(variant)
    filename = "data/variant_articles.json"
    save_to_json(filename, result)
    print(f"结果已保存到{filename}")

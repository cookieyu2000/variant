# function/get_pubmed_abstract.py

import requests
import xml.etree.ElementTree as ET
import os
import json

def fetch_pubmed_abstract(pubmed_id):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch article with PubMed ID {pubmed_id}")
        return None

def parse_pubmed_abstract(pubmed_id, xml_text):
    root = ET.fromstring(xml_text)
    abstract = ""
    title = ""
    authors = []
    
    article = root.find(".//PubmedArticle")
    if article is not None:
        title_node = article.find(".//ArticleTitle")
        if title_node is not None:
            title = title_node.text

        for author in article.findall(".//Author"):
            lastname = author.find("LastName")
            forename = author.find("ForeName")
            if lastname is not None and forename is not None:
                authors.append(f"{forename.text} {lastname.text}")

        abstract_node = article.find(".//AbstractText")
        if abstract_node is not None:
            abstract = abstract_node.text

    return {
        "pubmed_id": pubmed_id,
        "title": title,
        "authors": ", ".join(authors),  # 将作者列表转换为单行字符串
        "abstract": abstract
}

def save_pubmed_abstract(pubmed_id, data):
    os.makedirs('data', exist_ok=True)
    filename = "data/pubmed_text.json"
    existing_data = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

    # 添加新的数据
    existing_data.append(data)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


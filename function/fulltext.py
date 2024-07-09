import requests
import json
import os
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 計數器和文件索引初始化
data_counter = 0
file_index = 1
processed_pmids_file = "data/nen/processed_pmids.json"

def save_data_json(data, pmid):
    '''
    存到json的function，一個json存入100筆資料
    '''
    global data_counter, file_index

    # 確保 data 資料夾存在
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # 確保 data/nen 資料夾存在
    if not os.path.exists("data/nen"):
        os.makedirs("data/nen")
    
    # 構造文件路徑
    filepath = f"data/nen/nen_{file_index}.json"
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    
    # 檢查資料是否已經存在
    if pmid not in existing_data:
        # 保存新的資料
        existing_data[pmid] = data
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        print(f"Data for PMID {pmid} has been saved in the '{filepath}' file.")
    else:
        print(f"Data for PMID {pmid} already exists.")
    
    # 顯示資料
    print(json.dumps(existing_data[pmid], ensure_ascii=False, indent=4))
    
    # 更新計數器
    data_counter += 1
    if data_counter >= 100:
        data_counter = 0
        file_index += 1

    # 記錄已處理的 PMID
    with open(processed_pmids_file, "a", encoding='utf-8') as f:
        f.write(f"{pmid}\n")

def fetch_pubmed_data(pmid):
    '''
    呼叫api取得資料
    '''
    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids={pmid}&full=true"
    
    # 設置重試機制
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def fetch_pubmed_title(pmid):
    '''
    呼叫PubMed API抓取文章標題
    '''
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if 'result' in result and str(pmid) in result['result']:
                title = result['result'][str(pmid)].get('title', None)
                return title
            else:
                print(f"No title found for PMID {pmid}")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_relevant_data(data):
    '''
    抓取需要的資料
    '''
    sections = defaultdict(list)
    biotype_dict = defaultdict(set)
    title = None

    for passage in data.get('passages', []):
        section_type = passage['infons'].get('section_type')
        passage_type = passage['infons'].get('type')

        # 檢查是否為標題
        if (section_type == 'TITLE' or passage_type == 'title') and passage['text'] != "References":
            title = passage['text']
        
        # 篩選其他部分的文本
        if section_type and section_type not in ['REF', 'TITLE']:
            sections[section_type].append(passage['text'])
        elif passage_type == 'abstract':
            sections['abstract'].append(passage['text'])
        
        # 抓取biotype資料
        for annotation in passage.get('annotations', []):
            biotype = annotation['infons'].get('type')
            name = annotation['text']
            if biotype in ['Gene', 'Disease', 'Variant', 'Species'] and name:
                biotype_dict[biotype].add(name)
    
    # 將 set 轉換為 list
    biotype_dict = {k: list(v) for k, v in biotype_dict.items()}
    
    return sections, biotype_dict, title

def process_pmids_from_file(file_path):
    '''
    存入json的格式
    '''
    processed_pmids = set()
    if os.path.exists(processed_pmids_file):
        with open(processed_pmids_file, 'r', encoding='utf-8') as f:
            processed_pmids = set(line.strip() for line in f)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    for record in records:
        pmid = record['ID']
        if pmid in processed_pmids:
            print(f"PMID {pmid} 已處理，跳過")
            continue
        
        hgmd_class = record['label']
        data = fetch_pubmed_data(pmid)
        
        if data:
            sections, biotype_dict, _ = extract_relevant_data(data['PubTator3'][0])
            title = fetch_pubmed_title(pmid)
            result = {
                "title": title,
                "text": sections,
                "biotype": biotype_dict,
                "HGMD_class": hgmd_class
            }
            save_data_json(result, pmid)
        else:
            print(f"Failed to fetch data for PMID {pmid}.")

if __name__ == "__main__":
    file_path = "data/pub_cls.json"
    process_pmids_from_file(file_path)

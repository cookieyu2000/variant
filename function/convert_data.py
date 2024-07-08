# function/convert_data.py
import os
import pandas as pd


# 將Excel文件轉換為HDF5格式
def convert_excel_to_hdf5(excel_path, hdf5_path):
    print(f"Converting {excel_path} to {hdf5_path}...")
    file = pd.read_excel(excel_path)
    file.to_hdf(hdf5_path, key='data', mode='w')
    print("Conversion complete.")

# 讀取HDF5文件
def extract_headers_from_hdf5(hdf5_path):
    file = pd.read_hdf(hdf5_path, key='data', stop=0)
    headers = file.columns.tolist()
    print("Column Headers:", headers)
    return headers

def data():
    excel_path = 'data/HGMD_ann.xlsx'
    hdf5_path = 'data/HGMD_ann.h5'
    
    # 檢查HDF5文件是否存在，如果不存在則進行轉換
    if not os.path.exists(hdf5_path):
        convert_excel_to_hdf5(excel_path, hdf5_path)
    
    headers = extract_headers_from_hdf5(hdf5_path)
    print(headers)

def search_excel_by_keyword(keyword):
    hdf5_path = 'data/HGMD_ann.h5'
    if not os.path.exists(hdf5_path):
        convert_excel_to_hdf5('data/HGMD_ann.xlsx', hdf5_path)
    
    file = pd.read_hdf(hdf5_path, key='data')
    keyword_lower = keyword.lower()
    result = file[file.apply(lambda row: row.astype(str).str.lower().str.contains(keyword_lower).any(), axis=1)]

def filter_excel_by_columns(filters):
    hdf5_path = 'data/HGMD_ann.h5'
    if not os.path.exists(hdf5_path):
        convert_excel_to_hdf5('data/HGMD_ann.xlsx', hdf5_path)
    
    file = pd.read_hdf(hdf5_path, key='data')
    for column in filters.keys():
        if column.lower() not in map(str.lower, file.columns):
            print(f"列 '{column}' 不存在。")
            return
    
    result = file.copy()
    for column, value in filters.items():
        column_lower = next(col for col in file.columns if col.lower() == column.lower())
        result = result[result[column_lower].astype(str).str.lower().str.contains(value.lower())]

        
# main.py

from function.data_clinical_significance import *
from function.get_variant_publications import *
from function.search_variant import *
from function.excel import *
from function.get_pubmed_abstract import *
from function.variant_articles import *


def main_menu():
    while True:
        print("主選單:")
        print("1. 查詢變異體資料")
        print("2. 查詢Variant ID (RS ID)相關文章")
        print("3. 查詢Variant ID (RS ID)臨床意義")
        print("4. 按列篩選Excel數據")
        print("5. 查詢PubMed文章摘要")
        print("6. 輸入Variant查詢相關文章")
        print("exit. 退出程式")
        choice = input("請選擇功能: ")

        if choice == '1':
            while True:
                print("以選擇查詢變異體資料功能")
                query = input("請輸入查詢參數 (輸入 'exit' 返回主選單): ")

                if query.lower() == 'exit':
                    break

                search_variant(query)
        elif choice == '2':
            while True:
                print("以選擇查詢Variant ID (RS ID)相關文章功能")
                variant_id = input("請輸入Variant ID (RS ID) (輸入 'exit' 返回主選單): ")

                if variant_id.lower() == 'exit':
                    break

                get_variant_publications(variant_id)
                
        elif choice == '3':
            while True:
                print("以選擇查詢Variant ID (RS I4D)臨床意義功能")
                variant_id = input("請輸入Variant ID (RS ID) (輸入 'exit' 返回主選單): ")

                if variant_id.lower() == 'exit':
                    break

                data_clinical_significance(variant_id)
        
        elif choice == '4':
            print("以選擇按列篩選Excel數據功能")
            hdf5_path = 'data/HGMD_ann.h5'
            file = pd.read_hdf(hdf5_path, key='data')
            show_dataframe(file)


        elif choice == '5':
            while True:
                print("以選擇查詢PubMed摘要功能")
                pubmed_id = input("請輸入PubMed ID (輸入 'exit' 返回主選單): ")

                if pubmed_id.lower() == 'exit':
                    break

                xml_text = fetch_pubmed_abstract(pubmed_id)
                if xml_text:
                    article_data = parse_pubmed_abstract(pubmed_id, xml_text)
                    print(json.dumps(article_data, indent=4, ensure_ascii=False))
                    save_pubmed_abstract(pubmed_id, article_data)

        elif choice == '6':
            while True:
                print("以選擇輸入Variant查詢相關文章功能")
                variant = input("請輸入Variant (輸入 'exit' 返回主選單): ")

                if variant.lower() == 'exit':
                    break

                save_variant_articles(variant)

        elif choice == 'exit':
            print("程式已退出")
            break
        else:
            print("無效的選擇，請重新選擇。")

if __name__ == "__main__":
    main_menu()



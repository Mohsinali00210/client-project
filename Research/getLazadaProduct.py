import csv
import os
import random
import time
from typing import List
import requests
from .models import Item  # Ensure this is your Django model
import pandas as pd
import json
import random
KEYWORD = 'books'

def django_models_to_csv(models: List[Item], csv_file_path: str):
    try:
        # Extract data from models into a list of dictionaries
        data = [model.__dict__ for model in models]
        
        # Get field names (keys from the first dictionary)
        fieldnames = data[0].keys()
        
        # Check if the file already exists
        file_exists = os.path.exists(csv_file_path)
        
        # Open the file in append mode
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header only if the file is newly created
            if not file_exists:
                writer.writeheader()
            
            # Write the rows of data
            writer.writerows(data)
    except Exception as e:
        print(e)
        print("An error occurred while writing data to the CSV file")

USER_AGENTS = [ 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0', 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' ]


def searchDarazProducts(origin:str='pk',keyword:str='latest',pageNumber :str=1,priceRange:str="",rating:str="",sort:str ="",category:str="",brand:str="",location:str=""):
    try:
        session = requests.Session()
        headers = {
            'Referer': 'https://www.daraz.pk/',
            'User-Agent': USER_AGENTS[0]
        }
        keyword=keyword.strip()
        keyword=keyword.replace("  ","")
        if(origin =="bd" or origin=="np"):
            origin="com."+origin
        catalog="catalog"
        if category !="":
            catalog=category
        
        if brand !="":
            catalog+=f"/{brand}"
        
        url=f'https://www.daraz.{origin}/{catalog}/?ajax=true&isFirstRequest=true&page={pageNumber}'
        if keyword !="":
            url+=f'&q={keyword}'
        if location !="":
            url+=f'&location={location}'
        

        if sort !="":
            url+="&from=filter&sort="+sort
        if priceRange !="":
            url+="&price="+priceRange
        if rating !="":
            url+="&rating="+rating
        data = session.get(url, headers=headers).json()
        total_items = int(data['mainInfo']['totalResults'])
        page_size = int(data['mainInfo']['pageSize'])
        print(f'Total items: {total_items}, Page size: {page_size}')
        totalPage=total_items // page_size
        # Process the first page
        brands: List[dict] = data['mods']['filter']['filterItems']
        items: List[dict] = data['mods']['listItems']
        filteredQuatity= data['mods']['filter']['filteredQuatity']

        
        queryProductsBySKUUrl = f'https://www.daraz.{origin}/shop/site/api/queryProductsBySKU?&skus='
        queryProductsBySKUUrl += ",".join(i['skus'][0]['id'] for i in items)
        queryProductsBySKU = session.get(queryProductsBySKUUrl, headers=headers).json()
        queryProducts: List[dict] = queryProductsBySKU['result']['products']
        productData={}
        df1 = pd.DataFrame(items)
        df2 = pd.DataFrame(queryProducts)
        df1['SKU_id'] = df1['skus'].apply(lambda x: x[0]['id'] if isinstance(x, list) and len(x) > 0 else None)
        pd.set_option('display.max_columns', None)
        # Perform the join (merge) on the extracted 'SKU_id' and 'sku' from df2
        joined_df = pd.merge(df1, df2, left_on="SKU_id", right_on="sku", how="inner")
        joined_df['volumePayOrdPrdQty1d'] = joined_df['volumePayOrdPrdQty1w'].apply(
            lambda x: int(round(x / 7)) if x > 0 else 0
        )        

        joined_data = joined_df.to_dict(orient='records')   
        # Convert the result back to a list of dictionaries
        # joined_list = joined_df.to_dict(orient="records")
        # for index,item in enumerate(items):
        #     productData[index] ={**item,**queryProducts[index]}

        # django_items = [Item(**prepare_item_data(item)) for item in productData.values()]
        print("all products")
        print(joined_df)
        
        return joined_data,totalPage,filteredQuatity,brands
    except Exception as e:
        print(e)
        print("An error occurred while fetching data from Daraz")
        raise e



def searchLazadaProducts(origin:str='my',keyword:str='latest',pageNumber :str=1,priceRange:str="",rating:str="",sort:str ="",category:str="",brand:str="",location:str=""):
    try:
        session = requests.Session()
        user_agent = random.choice(USER_AGENTS)
        headers = {
            'Referer': f'https://www.lazada.{origin}/',
            'User-Agent': USER_AGENTS[0],
            "Accept-Language": "en-US,en;q=0.9", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Connection": "keep-alive"
        }
        headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 Edg/131.0.0.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': f'https://www.lazada.{origin}/',
    'User-Agent': USER_AGENTS[0],
    "Accept-Language": "en-US,en;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    'Connection': 'keep-alive',
    "content-type":"application/json; charset=utf-8",
    'Cookie': 'SID=g.a000qQhC1o1_hLdRuTWFWI4f7X2zMxP3NJPKf9dKHpD2CH1vYVCV5ykf73tr9F-oA4U8Z4Wd1QACgYKAQUSARQSFQHGX2MiskQuMSE2GQ8V-NG4_oxtFRoVAUF8yKrY_FtRpzODLsJBswGdkfNX0076; __Secure-1PSID=g.a000qQhC1o1_hLdRuTWFWI4f7X2zMxP3NJPKf9dKHpD2CH1vYVCVszZmmMQqRavEfQrRvhzefAACgYKASkSARQSFQHGX2MixLvjkncPVjLiExwB8UemQBoVAUF8yKoqeBT-TGVGk_7YTrwPNrEa0076; __Secure-3PSID=g.a000qQhC1o1_hLdRuTWFWI4f7X2zMxP3NJPKf9dKHpD2CH1vYVCVXV3T6Hs-C_7Czdra_6Lt1AACgYKAQcSARQSFQHGX2MitrZ4Tfrx5Yui_w3SlLivdhoVAUF8yKoBjTZhrwiYt7dAeYKhWwJx0076; HSID=ANj5IybbaHCS0XSnK; SSID=ATd1Wri5X4_qPKWGh; APISID=gzMwjFW7PgH766rY/A-7GvzSsuBgX8mjWC; SAPISID=JutvRIxl0eXQmGWp/AmVyuQIBsrj_lxjBd; __Secure-1PAPISID=JutvRIxl0eXQmGWp/AmVyuQIBsrj_lxjBd; __Secure-3PAPISID=JutvRIxl0eXQmGWp/AmVyuQIBsrj_lxjBd; SEARCH_SAMESITE=CgQI0JwB; OTZ=7834378_88_88_104280_84_446940; AEC=AZ6Zc-W6z61xnZbKC_tHaeHZIYzEyFQJpEAibJZHCfDWGD4yawdVLLqpYpA; NID=519=lcqQfoTtk0ll-FSwVwPr9xHLgyMu8dFEOdSMt3yStPqQ48D0Zm_TRPEdf5Vc8wpG2DHG60ZhqqCskkRgEwAVbfVMKYGOaO9Ohh6L8Sklf3bSOnG9aR5TROe8HX_Hnax3HYt1MNAjHN9ZAiBztUD5KgPpJSQw5ctU2j2KkDRTeDwwe-B29387byqB8q78NTXOOUAMS7Vg7qLNPVcyTO6HIinkv2IHkY-qxboi5eC8-yY4ufXLQNueUqrOMdxd6QpmqeHoEHzcPKsRxU2ZZ1_E2rDuUMBlh_LSYiG1npTF-yGAbTv5IHVF2Djx6j0RjUEe1XRT5hhQJ8LkVe_Ys94ai5vlog; __Secure-1PSIDTS=sidts-CjIBQT4rXwu-NdnP2WPvSAXzVK35B2TwTIwNjeekpKIlIXKuxkQQ3PPnSNx8lzE1_5e-RRAA; __Secure-3PSIDTS=sidts-CjIBQT4rXwu-NdnP2WPvSAXzVK35B2TwTIwNjeekpKIlIXKuxkQQ3PPnSNx8lzE1_5e-RRAA; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNzMyNTI1NTA2MDQzMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDI0ODY3NjM1MgogIGxvbmdpdHVkZV9lNzogNjcwODI2NDk2Cn0KcmFkaXVzOiA0MzEwNDY4LjM0MDAwNTIzOTUKcHJvdmVuYW5jZTogNgo=; SIDCC=AKEyXzXxLkfx5ynuMZ1iGdz8sHMzQCsZaYRqjUAF2MePT2wdtIkmNChAkMBUV6hFaBxODs5Yd7c; __Secure-1PSIDCC=AKEyXzUlzlLKUQ5vN0sNASyh6-dxHY-LFBIXJEWYC_2E-jGU9fKz9uuOhuqNTAT-yFhnR8FPog; __Secure-3PSIDCC=AKEyXzWA0F8wM33Fzf_2br1ESnTsRXwwfVAKGEpuRzeImMJE5Ori7iLuMupXNlxJd1pDlpFXkfQ'
}
        keyword=keyword.strip()
        keyword=keyword.replace("  ","")
        keyword =keyword.replace(" ","-")
        url=f'https://www.lazada.{origin}/tag/{keyword}/?ajax=true&page={pageNumber}'
        if brand !="":
                url=f'https://www.lazada.{origin}/{brand}/?ajax=true&page={pageNumber}'
        if keyword !="":
            url+=f"&q={keyword}"    
        catalog="tag"
        if category !="" and category is not None:
            catalog=category
            if brand !="":
                catalog=f"/{brand}"
            url=f'https://www.lazada.{origin}/{catalog}/?ajax=true&page={pageNumber}'
        
        if priceRange !="":
            url+="&price="+priceRange
        if rating !="":
            url+="&rating="+rating
        if sort !="" and sort is not None:
            url+="&from=filter&sort="+sort
        # data = session.get(url, headers=headers).json()
        response = session.get(url, headers=headers)
        joined_data=[]
        filteredQuatity=[]
        brands=[]
        data = {}
        totalPage=0
        print(url)
        # Check if the response contains data and if it's a valid JSON response
        if response.status_code == 200 and response.text.strip():  # Check if the response is not empty
            try:
                try:
                    data=response.json()  
                    print(data)

                except ValueError:
                    print("Error: invalid json format")
                    data=None
                if data:
                    total_items = int(data['mainInfo']['totalResults'])
                    page_size = int(data['mainInfo']['pageSize'])
                    print(f'Total items: {total_items}, Page size: {page_size}')
                    totalPage=total_items // page_size
                    # Process the first page
                    brands: List[dict] = data['mods']['filter']['filterItems']
                    items: List[dict] = data['mods']['listItems']
                    filteredQuatity= data['mods']['filter']['filteredQuatity']

                    queryProductsBySKUUrl = f'https://www.lazada.{origin}/shop/site/api/queryProductsBySKU?&skus='
                    queryProductsBySKUUrl += ",".join(i['skus'][0]['id'] for i in items)
                    queryProductsBySKU = session.get(queryProductsBySKUUrl, headers=headers).json()
                    
                    queryProducts: List[dict] = queryProductsBySKU['result']['products']

                    df1 = pd.DataFrame(items)
                    df2 = pd.DataFrame(queryProducts)
                    df1['SKU_id'] = df1['skus'].apply(lambda x: x[0]['id'] if isinstance(x, list) and len(x) > 0 else None)
                    pd.set_option('display.max_columns', None)
                    # Perform the join (merge) on the extracted 'SKU_id' and 'sku' from df2
                    joined_df = pd.merge(df1, df2, left_on="SKU_id", right_on="sku", how="inner")
                    joined_df['volumePayOrdPrdQty1d'] = joined_df['volumePayOrdPrdQty1w'].apply(
                        lambda x: int(round(x / 7)) if x > 0 else 0
                    )        
                    # joined_df['priceShow'] = joined_df['priceShow'].replace({'RM': '', ',': ''}, regex=True).astype(float)
                    joined_df['priceShow_x'] = joined_df['priceShow'].replace({'RM': '', ',': ''}, regex=True).astype(float)
                    joined_df['volumePayOrdPrdSales1d'] = joined_df['volumePayOrdPrdQty1d'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSales1w'] = joined_df['volumePayOrdPrdQty1w'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSales1m'] = joined_df['volumePayOrdPrdQty1m'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSalesStd'] = joined_df['volumePayOrdPrdQtyStd'] * joined_df['priceShow_x']

                    joined_data = joined_df.to_dict(orient='records')
                    print("all products")
                    print(joined_data)
            except ValueError:
                print("Error: value Error Accurred")
        else:
            print("No data or invalid response received.")
            data = None  # or handle the error as needed

        
        
        return joined_data,totalPage,filteredQuatity,brands
    except Exception as e:
        print(e)
        print("An error occurred while fetching data from Daraz")
        raise e
def getLazadaCategories():
    with open('./Research/lazada_categories_data.json', 'r',encoding='utf-8') as file:
        data = json.load(file)

    level2TabList = []
    categories = data['data']['resultValue']['categoriesLpMultiFloor']['data']
    for category in categories:
        level2TabList.append(category)
    return level2TabList

def prepare_item_data(data):
    return {
        'name': data.get('name', ""),
        'item_id': data.get('itemId', ""),
        'original_price': float(data.get('originalPrice', -1)),
        'price': float(data.get('price', -1)),
        'discount': data.get("discount")[:-4] if isinstance(data.get("discount"), str) else data.get("discount"),
        'rating': round(float(data.get('ratingScore', 0) or 0), 2),
        'review': int(data.get('review', 0) or 0),
        'location': data.get('location', ""),
        'seller_name': data.get('sellerName', ""),
        'seller_id': data.get('sellerId', ""),
        'item_sold': data.get("itemSoldCntShow", "0 sold")[:-5],
        'item_url': data.get('itemUrl', ""),
        'image_url': data.get('image', ""),
        'ProductQty1w': data.get('volumePayOrdPrdQty1w', ""),
        'ProductQty1m': data.get('volumePayOrdPrdQty1m', ""),
        'ProductQtyStd': data.get('volumePayOrdPrdQtyStd', "")

    }



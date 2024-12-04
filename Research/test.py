import csv
import os
import random
import time
from typing import List
import requests
# from .models import Item  # Ensure this is your Django model

KEYWORD = 'books'

# def django_models_to_csv(models: List[Item], csv_file_path: str):
#     try:
#         # Extract data from models into a list of dictionaries
#         data = [model.__dict__ for model in models]
        
#         # Get field names (keys from the first dictionary)
#         fieldnames = data[0].keys()
        
#         # Check if the file already exists
#         file_exists = os.path.exists(csv_file_path)
        
#         # Open the file in append mode
#         with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
            
#             # Write header only if the file is newly created
#             if not file_exists:
#                 writer.writeheader()
            
#             # Write the rows of data
#             writer.writerows(data)
#     except Exception as e:
#         print(e)
#         print("An error occurred while writing data to the CSV file")

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
]

def searchLazadaProducts(keyword:str='latest',pageNumber :str=1,priceRange:str="",rating:str=""):
    try:
        session = requests.Session()
        headers = {
            'Referer': 'https://www.lazada.com.my/',
            'User-Agent': USER_AGENTS[0]
        }
        keyword=keyword.strip()
        keyword=keyword.replace("  ","")
        keyword =keyword.replace(" ","-")
        url=f'https://www.lazada.com.my/tag/{keyword}/?ajax=true&page={pageNumber}'
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
        items: List[dict] = data['mods']['listItems']
        # items_ids= items['skus']['id']
        queryProductsBySKUUrl = 'https://www.lazada.com.my/shop/site/api/queryProductsBySKU?&skus='
        queryProductsBySKUUrl += ",".join(i['skus'][0]['id'] for i in items)
        queryProductsBySKU = session.get(queryProductsBySKUUrl, headers=headers).json()
        queryProducts: List[dict] = queryProductsBySKU['result']['products']
        productData={}
        for index,item in enumerate(items):
            productData[index] ={**item,**queryProducts[index]}
        print(productData)
        # django_items = [Item(**prepare_item_data(item)) for item in items]
        
     
    except Exception as e:
        print(e)
        print("An error occurred while fetching data from Daraz")
        raise e

def prepare_item_data(data):
    return {
        'name': data.get('name', ""),
        'item_id': data.get('itemId', ""),
        'original_price': float(data.get('originalPrice', -1)),
        'price': float(data.get('price', -1)),
        'discount': data.get('discount', " off")[:-4],
        'rating': round(float(data.get('ratingScore', 0) or 0), 2),
        'review': int(data.get('review', 0) or 0),
        'location': data.get('location', ""),
        'seller_name': data.get('sellerName', ""),
        'seller_id': data.get('sellerId', ""),
        'item_sold': data.get("itemSoldCntShow", "0 sold")[:-5],
        'item_url': data.get('itemUrl', ""),
        'image_url': data.get('image', "")
    }

searchLazadaProducts('ear buds',1,"2-20000","2-5")

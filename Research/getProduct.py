import csv
import os
import random
import time
from typing import List
import requests
from .models import Item  # Ensure this is your Django model


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

import json
from rake_nltk import Rake
import nltk
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
# Download the stopwords resource
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
# Initialize Rake (without stopwords, using English stopwords from NLTK)
r = Rake(stopwords=["the", "is", "in", "at"])
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
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

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
]

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
        if category !="" and category is not None:
            catalog=category
        if brand !="":
            catalog+=f"/{brand}"
        url=f'https://www.daraz.{origin}/{catalog}/?ajax=true&isFirstRequest=true&page={pageNumber}'
        if keyword !="":
            url+=f'&q={keyword}'
        if location !="":
            url+=f'&location={location}'
        if sort !="" and sort is not None:
            url+="&from=filter&sort="+sort
        if priceRange !="":
            url+="&price="+priceRange
        if rating !="":
            url+="&rating="+rating
        response = session.get(url, headers=headers)
        joined_data=[]
        filteredQuatity=[]
        brands=[]
        totalPage=0
        print(url)
        joined_df=pd.DataFrame()
        # Check if the response contains data and if it's a valid JSON response
        if response.status_code == 200 and response.text.strip():  # Check if the response is not empty
            try:
                data = response.json()
                total_items = int(data['mainInfo']['totalResults'])
                page_size = int(data['mainInfo']['pageSize'])
                print(f'Total items: {total_items}, Page size: {page_size}')
                totalPage=total_items // page_size
                # Process the first page
                brands: List[dict] = data['mods']['filter']['filterItems']
                items: List[dict] = data['mods']['listItems']
                if total_items>0:
                    print(items)
                    filteredQuatity= data['mods']['filter']['filteredQuatity']
                    queryProductsBySKUUrl = f'https://www.daraz.{origin}/shop/site/api/queryProductsBySKU?&skus='
                    queryProductsBySKUUrl += ",".join(i['skus'][0]['id'] for i in items)
                    queryProductsBySKU = session.get(queryProductsBySKUUrl, headers=headers).json()
                    queryProducts: List[dict] = queryProductsBySKU['result']['products']
                    productData={}
                    df1 = pd.DataFrame(items)
                    df2 = pd.DataFrame(queryProducts)
                    df1 = df1.fillna(0)
                    df2 = df2.fillna(0)
                    df1['SKU_id'] = df1['skus'].apply(lambda x: x[0]['id'] if isinstance(x, list) and len(x) > 0 else None)
                    pd.set_option('display.max_columns', None)
                    # Perform the join (merge) on the extracted 'SKU_id' and 'sku' from df2
                    joined_df = pd.merge(df1, df2, left_on="SKU_id", right_on="sku", how="inner")
                    joined_df['volumePayOrdPrdQty1d'] = joined_df['volumePayOrdPrdQty1w'].apply(
                        lambda x: float(round(x / 7)) if x > 0 else 0
                    )        
                    # joined_df['priceShow'] = joined_df['priceShow'].replace({'Rs. ': '', ',': ''}, regex=True).astype(float)
                    joined_df['priceShow_x'] = joined_df['priceShow'].replace({'Rs. ': '', ',': ''}, regex=True).astype(float)
                    joined_df['volumePayOrdPrdSales1d'] = joined_df['volumePayOrdPrdQty1d'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSales1w'] = joined_df['volumePayOrdPrdQty1w'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSales1m'] = joined_df['volumePayOrdPrdQty1m'] * joined_df['priceShow_x']
                    joined_df['volumePayOrdPrdSalesStd'] = joined_df['volumePayOrdPrdQtyStd'] * joined_df['priceShow_x']

                    joined_data = joined_df.to_dict(orient='records')   
                    print("all products")
                    # print(joined_df)
                    print("items")
                    print("items")
                    print("items")
                    print("items")
                    print(df1)
                    print("all products")
                    print("all products")
                    print("all products")
                    print("all products")
                    print("all products")
                    print(df2)
                    print(url)
                    pd.set_option('display.max_columns', None)  # Show all columns
                    pd.set_option('display.width', None)
                    print(joined_df.dtypes)

                
            except ValueError:
                print("Error: Response is not valid JSON.")
                data = None  # or handle the error as needed
        else:
            print("No data or invalid response received.")
            data = None  # or handle the error as needed
        return joined_data,totalPage,filteredQuatity,brands
    except Exception as e:
        print(e)
        print("An error occurred while fetching data from Daraz")
        raise e


def prepare_item_data(data):
    return {
        'name': data.get('name', ""),
        'item_id': data.get('itemId', ""),
        'original_price': float(data.get('originalPrice', -1)),
        'price': float(float(data.get('priceShow', -1).replace("Rs. ", "").replace("৳ ","").replace(",",""))),
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






def create_web_driver(url: str) -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    # set chrome driver options to disable any popup's from the website
    # to find local path for chrome profile, open chrome browser
    # and in the address bar type, "chrome://version"
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    # To disable the message, "Chrome is being controlled by automated test software"
    chrome_options.add_argument("disable-infobars")
    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2
        })
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
 
    delay = 2 #secods
    WebDriverWait(driver, delay)
    print(type(driver))
    print ("Page is ready")
    # sleep(2)
    return driver
def findFrequency(text):
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases_with_scores()
    keyword_frequency = Counter(keywords)
    keyword_frequency = {keyword: keyword_frequency[keyword] for keyword in keyword_frequency}

    return keyword_frequency

def getDiscription(url: str):
    
    base_url = url
    print(base_url)
    browser = create_web_driver(base_url)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    return soup
   


# URL of the webpage you want to scrape
url = 'https://www.daraz.pk/products/air-31-earbuds-hi-fi-sound-quality-with-led-display-crystal-transparent-bluetooth-50-i562658816.html'  # Replace with the URL you want to scrape


def getProductBySKU(skus_dic):
    session = requests.Session()
    queryProducts=[]

    for item in skus_dic:
        Origin = item['Origin']
        SKUs = item['SKUs']
        headers = {
            'Referer': Origin+'/',
            'User-Agent': USER_AGENTS[0]
        }
        queryProductsBySKUUrl = Origin+'/shop/site/api/queryProductsBySKU?&skus='+SKUs
        queryProductsBySKU = session.get(queryProductsBySKUUrl, headers=headers).json()
        queryProducts.append(queryProductsBySKU['result']['products'])
    return queryProducts

def getCategories():
    with open('./Research/categories_data.json', 'r',encoding='utf-8') as file:
        data = json.load(file)

    level2TabList = []
    categories = data['data']['resultValue']['categoriesLpMultiFloor']['data']
    for category in categories:
        level2TabList.append(category)
    return level2TabList

def PrepareProductAndCollectionData(Collections,products):
    # Data: Collection and Product Data
    collection_Data = [
        {
            "collection_item_id": Collection.collection_item_id,
            "product_id": Collection.product_id,
            "price": Collection.price,
            "user_id": Collection.user_id,
            "oldPrice": Collection.oldPrice,
            "sku": Collection.SKU,
            "product_name": Collection.product_name,
            "product_url":Collection.product_url,
            "image_url": Collection.image_url,
            "brand_name": Collection.brand_name,
            "category": Collection.category,
            "date_time": Collection.date_time,
            "seller_id": Collection.seller_id,
            "seller_name": Collection.seller_name
        }
        for Collection in Collections
        
    ]
    product_Data=[]
    product_Data = []
    for product in products:
        if isinstance(product, dict):
            product_Data.append({
                'auctionId': product['auctionId'],
                'brandId': product['brandId'],
                'categories': product['categories'],
                'categoryId': product['categoryId'],
                'createdTime': product['createdTime'],
                'discount': product['discount'],
                'discountFormatted': product['discountFormatted'],
                'discountPrice':product['discountPrice'],
                'discountPriceFormatted': product['discountPriceFormatted'],
                'discountPriceFormattedRaw': product['discountPriceFormattedRaw'],
                'freeShipping': product['freeShipping'],
                'hitPromotion':product['hitPromotion'],
                'imageUrl': product['imageUrl'],
                'inStock': product['inStock'],
                'itemPromotionTags': product['itemPromotionTags'],
                'mobileUrl': product['mobileUrl'],
                'pdpUrl': product['pdpUrl'],
                'price': product['price'],
                'priceFormatted': product['priceFormatted'],
                'promotionEndTime': product['promotionEndTime'],
                'promotionStartTime': product['promotionStartTime'],
                'rating':product['rating'],
                'reviews': product['reviews'],
                'sellerId': product['sellerId'],
                'shopCategoryIds': product['shopCategoryIds'],
                'shopId': product['shopId'],
                'showItemFlag': product['showItemFlag'],
                'sku': product['sku'],
                'skuId': product['skuId'],
                'storeType': product['storeType'],
                'title': product['title'],
                'volumePayOrdPrdQty1m': product['volumePayOrdPrdQty1m'],
                'volumePayOrdPrdQty1w': product['volumePayOrdPrdQty1w'],
        
            } )
    

    return collection_Data,product_Data
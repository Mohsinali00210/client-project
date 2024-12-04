

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from time import sleep
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# import os
# from bs4 import BeautifulSoup
# import requests
# from bs4 import BeautifulSoup
# from rake_nltk import Rake
# import nltk
# from collections import Counter

# # # Download the stopwords resource
# # nltk.download('stopwords')
# # nltk.download('punkt')
# # nltk.download('punkt_tab')
# # # Initialize Rake (without stopwords, using English stopwords from NLTK)
# # r = Rake()
# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd

# def create_web_driver(url: str) -> WebDriver:
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-extensions")
#     # set chrome driver options to disable any popup's from the website
#     # to find local path for chrome profile, open chrome browser
#     # and in the address bar type, "chrome://version"
#     chrome_options.add_argument('disable-notifications')
#     chrome_options.add_argument('--disable-infobars')
#     chrome_options.add_argument('start-maximized')
#     # To disable the message, "Chrome is being controlled by automated test software"
#     chrome_options.add_argument("disable-infobars")
#     # Pass the argument 1 to allow and 2 to block
#     chrome_options.add_experimental_option("prefs", { 
#         "profile.default_content_setting_values.notifications": 2
#         })
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     driver.get(url)
 
#     delay = 2 #secods
#     WebDriverWait(driver, delay)
#     print(type(driver))
#     print ("Page is ready")
#     # sleep(2)
#     return driver
# def findFrequency(text):
#     # Create the vectorizer
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(text)

#     # Get the feature names (words)
#     feature_names = vectorizer.get_feature_names_out()

#     # Create a DataFrame to display the TF-IDF scores for each term in each document
#     df = pd.DataFrame(X.toarray(), columns=feature_names)

#     # Print the term frequencies (TF) and their corresponding TF-IDF scores for each document
#     print(df)
#     return df

# def getDiscription(url: str):
    
#     base_url = url
#     print(base_url)
#     browser = create_web_driver(base_url)
#     html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#     soup = BeautifulSoup(html, "html.parser")

#     return soup
   


# # URL of the webpage you want to scrape
# url = 'https://www.daraz.pk/products/air-31-earbuds-hi-fi-sound-quality-with-led-display-crystal-transparent-bluetooth-50-i562658816.html'  # Replace with the URL you want to scrape




# # Parse the HTML content of the page
# soup = getDiscription(url)
# discription_meta = soup.select('meta[name="description"]')
# titleElement = soup.select('title')

# description=''
# title=''
# descriptionDetail=[]
# # Find the <meta> tag with charset="utf-8"
# if discription_meta and 'content' in discription_meta[0].attrs:
#     description = discription_meta[0]['content']
#     descriptionDetail=description
#     keyword_frequency=findFrequency(descriptionDetail)
#     print("********************************")
#     # for score, keyword in keyword_frequency:
#     #     print(f"{keyword}, Score: {score}")
# if titleElement:
#     descriptionDetail[1]=titleElement[0].text

#     keyword_frequency=findFrequency(descriptionDetail)
#     print("********************************")
#     # for score, keyword in keyword_frequency:
#     #     print(f"{keyword}, Score: {score}")

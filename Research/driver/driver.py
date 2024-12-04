from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os

def create_web_driver(driver:webdriver.Chrome,url: str, location: str) -> WebDriver:
    driver.get(url)
    if location == 'shopee':
        return auto_login_shopee(driver)
    delay = 6 #secods
    WebDriverWait(driver, delay)
    print(type(driver))
    print ("Page is ready")
    sleep(30)
    return driver

def auto_login_shopee(driver: WebDriver) -> WebDriver:
    sleep(4)
    load_dotenv()

    username = os.getenv("username")
    password = os.getenv("password")

    if username is None or password is None:
        raise ValueError("Username or password not set in environment variables.")

    driver.find_element("name", "loginKey").send_keys(username)
    driver.find_element("name", "password").send_keys(password)
    sleep(3)
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button').click()

    WebDriverWait(driver=driver, timeout=8).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    print("Page is ready")
    sleep(20)
    return driver

# def auto_login_shopee(driver : WebDriver) -> WebDriver:
#     sleep(4)
#     load_dotenv()
    
#     username = os.getenv("username")
#     password = os.getenv("password")
    
#     driver.find_element("name", "loginKey").send_keys(username)
#     # find password input field and insert password as well
#     driver.find_element("name", "password").send_keys(password)
#     # click login button
#     sleep(3)
#     # click login button
#     driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button').click()

#     # wait the ready state to be complete
#     WebDriverWait(driver=driver, timeout=8).until(
#         lambda x: x.execute_script("return document.readyState === 'complete'")
#     )
#     print ("Page is ready")
#     sleep(20)
#     return driver

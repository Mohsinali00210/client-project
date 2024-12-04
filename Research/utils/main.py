from bs4 import BeautifulSoup
from tiki import tiki_scraper as tiki_scraper
from driver.driver import create_web_driver
from config import config
from lazada import lazada_scraper as lazada_scraper
from daraz import daraz_scraper as daraz_scraper
from shopee import shopee_scraper as shopee_scraper
from amazon import amazon_scraper as amazon_scraper

# from .tiki import tiki_scraper as tiki_scraper
# from .driver.driver import create_web_driver
# from .config import config
# from .lazada import lazada_scraper as lazada_scraper
# from .daraz import daraz_scraper as daraz_scraper
# from .shopee import shopee_scraper as shopee_scraper
# from .amazon import amazon_scraper as amazon_scraper


def shopping_online_run(location: str, keyword: str, page: str):
    # location, keyword, page = input_initial_value()

    shopping_online_info = config.ShoppingOnlineLocation(
        location=location, 
        keyword=keyword, 
        page=page,
    )

    base_url = shopping_online_info.get_base_url()
    print(base_url)
    browser = create_web_driver(base_url, location)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    match location:
        case "lazada":
            product_info = lazada_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
            print(product_info)
            return product_info
        case "daraz":
            product_info = daraz_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
            print(product_info)
            return product_info
        # case "shopee":
        #     is_choose = add_to_cart()
        #     if is_choose:
        #         index_item = int(input("Please fill item's index you want to add it in cart: "))
        #         shopee_scraper.add_product_to_cart(browser, soup, index_item)
        #     else:
        #         product_info = shopee_scraper.get_product_info(soup=soup)
        #         shopping_online_info.add_product_to_csv(product_info)

        
shopping_online_run("daraz", "earbuds", "1")

            
   
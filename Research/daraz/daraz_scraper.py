from bs4 import BeautifulSoup
from bs4.element import ResultSet
from typing import List, Generator



def get_product_names(soup: BeautifulSoup) -> ResultSet:
    selector = '.buTCk .RfADt a'
    name_items = soup.select(selector=selector)
    return name_items
def get_url(soup: BeautifulSoup) -> ResultSet:
    selector = '.ICdUp ._95X4G a'
    name_items = soup.select(selector=selector)
    urls = [item['href'] for item in name_items if 'href' in item.attrs]

    return urls
def get_img_src(soup: BeautifulSoup) -> ResultSet:
    selector = '.ICdUp ._95X4G a .jBwCF img'
    img_items = soup.select(selector=selector)
    image_src = [img['src'] for img in img_items if 'src' in img.attrs]

    return image_src
def get_rating_items(soup: BeautifulSoup) -> ResultSet:
    selector = '.buTCk ._6uN7R ._32vUv .qzqFw'
    price_items = soup.select(selector=selector)
    return price_items
def get_price_items(soup: BeautifulSoup) -> ResultSet:
    selector = '.buTCk .aBrP0 .ooOxS'
    price_items = soup.select(selector=selector)
    return price_items

def get_historical_sold(soup: BeautifulSoup) -> ResultSet:
    selector = '.buTCk ._6uN7R'
    sold_items = soup.select(selector=selector)
    return sold_items

def get_product_origin(soup: BeautifulSoup) -> ResultSet:
    selector = '.buTCk ._6uN7R .oa6ri'
    product_origin = soup.select(selector=selector)
    return product_origin

def get_sold_item_at_index(index: int, sold_items: ResultSet) -> str:
    sold_item = sold_items[index].select('._1cEkb')
    if len(sold_item) < 1:
        return str(0)
    return sold_item[0].text

def get_product_info(soup: BeautifulSoup) :
    selectors = '._17mcb .Bm3ON'
    cart_elements= soup.select(selector=selectors)
    i=0
    products =[]
    for cart_element in cart_elements:
        print(cart_element)
        title = cart_element.select_one('.RfADt a')['title']
        price = cart_element.select_one('.ooOxS').text.strip()
        url = cart_element.select_one('.RfADt a')['href']
        img_src = cart_element.select_one('.ICdUp ._95X4G a .jBwCF  img')['src']
        region = cart_element.select_one('._6uN7R .oa6ri').text.strip()

        # Assuming rating and sold information
        rating = cart_element.select_one('.mdmmT .qzqFw').text.strip() if cart_element.select_one('.mdmmT .qzqFw') else 'No rating'
        sold = cart_element.select_one('._6uN7R ._1cEkb').text.strip() if cart_element.select_one('._6uN7R ._1cEkb') else 'Not available'
        product_info = {
            'title': title,
            'price': price,
            'url': url,
            'img_src': img_src,
            'region': region,
            'rating': rating,
            'sold': sold,
        }
    
        
        products.append(product_info)
    return products
        # product_info = "{0} ,  {1} ,  {2} ,  {3}  ,  {4}  ,  {5}  ,  {6} \n".format(title, price, sold, region,url,img_src,rating)
        # yield product_info
    
    

# def get_product_names(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .buTCk .RfADt a'
#     name_items = soup.select(selector=selector)
#     return name_items
# def get_url(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .ICdUp ._95X4G a'
#     name_items = soup.select(selector=selector)
#     urls = [item['href'] for item in name_items if 'href' in item.attrs]

#     return urls
# def get_img_src(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .ICdUp ._95X4G a .jBwCF img'
#     img_items = soup.select(selector=selector)
#     image_src = [img['src'] for img in img_items if 'src' in img.attrs]

#     return image_src
# def get_rating_items(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .buTCk ._6uN7R ._32vUv .qzqFw'
#     price_items = soup.select(selector=selector)
#     return price_items
# def get_price_items(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .buTCk .aBrP0 .ooOxS'
#     price_items = soup.select(selector=selector)
#     return price_items

# def get_historical_sold(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .buTCk ._6uN7R'
#     sold_items = soup.select(selector=selector)
#     return sold_items

# def get_product_origin(soup: BeautifulSoup) -> ResultSet:
#     selector = '._17mcb .Bm3ON .buTCk ._6uN7R .oa6ri'
#     product_origin = soup.select(selector=selector)
#     return product_origin

# def get_sold_item_at_index(index: int, sold_items: ResultSet) -> str:
#     sold_item = sold_items[index].select('._1cEkb')
#     if len(sold_item) < 1:
#         return str(0)
#     return sold_item[0].text

# def get_product_info(soup: BeautifulSoup) :
#     name_items = get_product_names(soup=soup)
#     price_items = get_price_items(soup=soup)
#     sold_items = get_historical_sold(soup=soup)
#     product_origin = get_product_origin(soup=soup)
#     url = get_url(soup=soup)
#     img_src = get_img_src(soup=soup)
#     rating_item = get_rating_items(soup=soup)
    
#     for index in range(len(name_items)):
#         sold_item = get_sold_item_at_index(index, sold_items)
#         product_info = "{0} ,  {1} ,  {2} ,  {3}  ,  {4}  ,  {5}  ,  {6} \n".format(name_items[index]['title'], price_items[index].text, sold_item, product_origin[index].text,url[index],img_src[index],rating_item[index].text)
#         yield product_info
    
    
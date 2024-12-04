from django.shortcuts import render,redirect, get_object_or_404
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from .getProduct import getCategories,searchDarazProducts,getDiscription,findFrequency,getProductBySKU,PrepareProductAndCollectionData
from .getLazadaProduct import searchLazadaProducts,getLazadaCategories
from django.core.paginator import Paginator
from api.models import Collection,CollectionItems
# Create your views here.
from django.http import JsonResponse
from api.serializers import CollectionItemsSerializer
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from collections import defaultdict
from django.contrib.auth.decorators import login_required

# from rake_nltk import Rake
# import nltk
from collections import Counter
import json
import pandas as pd

# Download the stopwords resource
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab')
# # Initialize Rake (without stopwords, using English stopwords from NLTK)
# r = Rake()


from . import main
@login_required
def ProductDiscovery(request):
    categories= getCategories()
    lazadaCategories= getLazadaCategories()
    return render(request, 'product-discovery.html',{'categories':categories,'lazadaCategories':lazadaCategories})


@login_required
def Search_Discovery(request):
    keyword = request.GET.get('keyword', '') or request.POST.get('keyword', '')
    price_min = request.GET.get('price_min') or request.POST.get('price_min') or ''
    price_max = request.GET.get('price_max') or request.POST.get('price_max') or ''
    rating_min = request.GET.get('rating_min') or request.POST.get('rating_min') or ''
    rating_max = request.GET.get('rating_max') or request.POST.get('rating_max')
    orders_min = request.GET.get('orders_min') or request.POST.get('orders_min')
    orders_max = request.GET.get('orders_max') or request.POST.get('orders_max')
    reviews_min = request.GET.get('reviews_min') or request.POST.get('reviews_min')
    reviews_max = request.GET.get('reviews_max') or request.POST.get('reviews_max')
    origin = request.GET.get('origin') or request.POST.get('origin')
    Plateform = request.GET.get('Plateform') or request.POST.get('Plateform')
    page = request.GET.get('page') or request.POST.get('page')
    sort = request.GET.get('sort') or request.POST.get('sort')
    category = request.GET.get('category') or request.POST.get('category')
    LZCategory = request.GET.get('category') or request.POST.get('category')
    brand = request.GET.get('brand') or request.POST.get('brand') or ""
    location = request.GET.get('location') or request.POST.get('location') or ""
    priceRange=""
    categories= getCategories()
    lazadaCategories= getLazadaCategories()
    products=[]
    filteredQuatity=""
    pages=0
    if not page:
        page=1
    if price_min !="" or price_max!="":
        priceRange=price_min+"-"+price_max
    if keyword!="" or priceRange!="" or rating_min!="" or origin!="" or Plateform!="" or sort!="" or category!="":
        if Plateform =='lazada':
            products,pages,filteredQuatity,filterOptions=searchLazadaProducts(origin,keyword,page,priceRange,rating_min,sort,category,brand,location)
        if Plateform == 'daraz':
            products,pages,filteredQuatity,filterOptions=searchDarazProducts(origin,keyword,page,priceRange,rating_min,sort,category,brand,location)
    
    pages = int(pages)
    pag=list(range(1, pages))
    return render(request,  'product-discovery.html', {'products': products,'categories':categories,'lazadaCategories':lazadaCategories,"PageNum":pag,"filteredQuatity":filteredQuatity,"filterOptions":filterOptions})

@login_required
def mycollections(request):
    CurrentUserId = request.user.id
    Collections = Collection.objects.filter(user_id=CurrentUserId)
    print(Collections)
    return render(request, 'mycollections.html',{"collections":Collections})
@login_required
def DeshboardView(request):
    return render(request, 'index.html')
@login_required
def StoreDiscoveryView(request):
    return render(request, 'Store_Discovery.html')

def get_collection(request, collection):
    # Filter the collection items
    collection_items = CollectionItems.objects.filter(collection_id=collection)
    
    if collection_items.exists():
        # Construct the JSON response manually
        items_data = [
            {
                "collection_item_id": item.collection_item_id,
                "product_id": item.product_id,
                "price": item.price,
                "oldPrice": item.oldPrice,
                "SKU": item.SKU,
                "product_name": item.product_name,
                "product_url": item.product_url,
                "image_url": item.image_url,
                "brand_name": item.brand_name,
                "category": item.category,
                "date_time": item.date_time,
                "seller_id": item.seller_id,
                "seller_name": item.seller_name
            }
            for item in collection_items
        ]
        
        return JsonResponse(items_data, safe=False)
    else:
        return JsonResponse({"error": "Collection not found"}, status=404)

def FindKeyword(request):
    

    # URL of the webpage you want to scrape
    ProductLink = request.GET.get('ProductLink', '') or request.POST.get('ProductLink', '')

    title=[]
    description_frequency=[]
    title_frequency=[]
    if ProductLink:

        # Parse the HTML content of the page
        soup = getDiscription(ProductLink)
        discription_meta = soup.select('meta[name="description"]')
        titleElement = soup.select('title')

        description=''
        title=''
        # Find the <meta> tag with charset="utf-8"
        if discription_meta and 'content' in discription_meta[0].attrs:
            description = discription_meta[0]['content']
            description_frequency=findFrequency(description)
        if titleElement:
            title=titleElement[0].text
            title_frequency=findFrequency(title)
    return render(request, 'FindKeywords.html',{"title_frequency":title_frequency,"description_frequency":description_frequency})

@login_required
def DeleteCollection(request, collectionId):
    CurrentUserId = request.user.id

    collection = get_object_or_404(Collection, collection_id=collectionId, user_id=CurrentUserId)
    collection.delete()
    return redirect('my_collections')
@login_required
def DeleteCollectionItem(request, collectionItemId):
    CurrentUserId = request.user.id
    collection = get_object_or_404(CollectionItems,collection_item_id=collectionItemId, user_id=CurrentUserId)
    collection.delete()
    return JsonResponse({"response": "Collection Item deleted"}, status=200)
    
    
from django.core.mail import send_mail
from django.conf import settings

@login_required
def sendMail(request):
    collectionitems=CollectionItems.objects.all()

    # Use the .values() method to convert the QuerySet into a list of dictionaries
    collectionitems_data = list(collectionitems.values())

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(collectionitems_data)
    SKUS=''
    
    skus_dic=[]
    grouped_skus = defaultdict(list)
    for item in collectionitems:
        grouped_skus[item.origin].append(item.SKU)

    for origin, skus in grouped_skus.items():
        joined_skus = ",".join(skus)
        skus_dic.append({
            'Origin':origin,
            'SKUs':joined_skus
        })
    # SKUS += ",".join(i.SKU for i in collectionitems)
    products=getProductBySKU(skus_dic)
    Collection_Data,Product_Data=PrepareProductAndCollectionData(collectionitems,products)
    # Set pandas options to display full content in all columns and rows
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)     # Show all rows
    pd.set_option('display.max_colwidth', None) # Don't truncate column content

    df1 = pd.DataFrame(Collection_Data)
    flat_products = [item[0] for item in products]  # Extract inner lists

    df2 = pd.DataFrame(flat_products)
    # df2 = pd.DataFrame(products[0])
    # Perform the join (merge) on the "id" column
    joined_df = pd.merge(df, df2, left_on="SKU",right_on="sku",how="inner")
    # Convert the result back to a list of dictionaries
    joined_list = joined_df.to_dict(orient="records")
    print(joined_list)
    for prd in joined_list:
        if prd['price_x']==prd['discountPrice']:
            users = User.objects.filter(id=prd['user_id'])
            for user in users:
                subject = 'Product Price has been Changed'
                message = f'the price of \"{prd['product_name']}\" has been change {prd['price_x']} from {prd['discountPrice']}.  Link {prd['product_url']}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]  # List of recipients

                response=send_mail(subject, message, from_email, recipient_list)
                print("email send to ",user.email)
    return render(request, 'send_mail.html',{"response":joined_list})



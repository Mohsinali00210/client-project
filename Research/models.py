from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255, blank=True)
    item_id = models.CharField(max_length=255, unique=True)
    original_price = models.FloatField(default=-1)
    price = models.FloatField(default=-1)
    discount = models.CharField(max_length=255, default=" off")
    rating = models.FloatField(default=0)
    review = models.IntegerField(default=0)
    location = models.CharField(max_length=255, blank=True)
    seller_name = models.CharField(max_length=255, blank=True)
    seller_id = models.CharField(max_length=255, blank=True)
    item_sold = models.CharField(max_length=255, default="0 sold")
    item_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    ProductQty1w = models.CharField(max_length=255, unique=True)
    ProductQty1m = models.CharField(max_length=255, unique=True)
    ProductQtyStd = models.CharField(max_length=255, unique=True)

    @classmethod
    def prepare_data(cls, data):
        data['name'] = data.get('name', "")
        data['item_id'] = data.get('itemId', "")
        data['original_price'] = float(data.get('originalPrice', -1))
        data['price'] = float(data.get('price', -1))
        data['discount'] = data.get('discount', " off")[:-4]
        data['rating'] = round(float(data.get('ratingScore', 0)), 2)
        data['review'] = int(data.get('review', 0))
        data['location'] = data.get('location', "")
        data['seller_name'] = data.get('sellerName', "")
        data['seller_id'] = data.get('sellerId', "")
        data['item_sold'] = data.get("itemSoldCntShow", "0 sold")[:-5]
        data['item_url'] = data.get('itemUrl', "")
        data['image_url'] = data.get('image', "")
        data['ProductQty1w'] = data.get('volumePayOrdPrdQty1w', "")
        data['ProductQty1m'] = data.get('volumePayOrdPrdQty1m', "")
        data['ProductQtyStd'] = data.get('volumePayOrdPrdQtyStd', "")
        return data
# models.py
from django.db import models

class Collection(models.Model):
    user_id = models.IntegerField()
    collection_id = models.AutoField(primary_key=True)
    collection_name = models.CharField(max_length=255)

class CollectionItems(models.Model):
    collection_item_id = models.AutoField(primary_key=True)
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    price = models.FloatField()
    oldPrice = models.FloatField(blank=True,null=True,default=0)
    SKU = models.CharField(max_length=255)
    origin = models.CharField(max_length=100,default='https://www.daraz.pk')
    product_name = models.CharField(max_length=255,default='default_value')
    product_url = models.CharField(max_length=255,default='default_value')
    image_url = models.CharField(max_length=255,default='default_value')
    brand_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    seller_id = models.IntegerField()
    seller_name = models.CharField(max_length=255)


class categoryCommision(models.Model):
    category_ids = models.CharField(max_length=20)

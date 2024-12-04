# serializers.py
from rest_framework import serializers
from .models import categoryCommision,Collection, CollectionItems

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItems
        fields = '__all__'
class CollectionItemsProductIdSerializer(serializers.ModelSerializer): 
    class Meta: model = CollectionItems 
    fields = ['product_id']
class categoryFetchSerializer(serializers.Serializer): 
    category_ids = serializers.ListField(
        child=serializers.CharField(),  # Use CharField to accept string IDs
        required=True,
        allow_empty=False,
        help_text="List of category IDs to fetch commissions for."
    )



class CategoryListSerializer(serializers.Serializer):
    category_ids = serializers.ListField(
        child=categoryFetchSerializer()  # Use CategorySerializer for each item
    )
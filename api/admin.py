from django.contrib import admin

# Register your models here.
from .models import Collection, CollectionItems

# Register Collection model
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('collection_id', 'user_id', 'collection_name')  # Columns in the list view
    search_fields = ('collection_name', 'user_id')  # Enable search by collection name and user id

# Register CollectionItems model
@admin.register(CollectionItems)
class CollectionItemsAdmin(admin.ModelAdmin):
    list_display = ('collection_item_id','user_id', 'product_name',"SKU","origin","price","oldPrice", 'product_id', 'collection_id', 'brand_name', 'seller_name', 'date_time')
    search_fields = ('product_name', 'product_id', 'brand_name', 'category')  # Enable search
    list_filter = ('category', 'brand_name')  # Optional: Add filters to filter by category or brand
    raw_id_fields = ('collection_id',)  # Use raw ID fields for ForeignKey fields to improve performance



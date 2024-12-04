from django.contrib import admin
from django.urls import path
from .views import sendMail,DeleteCollectionItem,DeleteCollection,FindKeyword,get_collection,ProductDiscovery,Search_Discovery,mycollections,StoreDiscoveryView,DeshboardView
urlpatterns = [
    path('', ProductDiscovery,name='productDiscovery'),
    path('search_products/', Search_Discovery,name='search_products'),
    path('mycollections/', mycollections,name='my_collections'),
    path('StoreDiscovery/', StoreDiscoveryView,name='Store_Discovery'),
    path('deshboard/', DeshboardView,name='deshboard'),
    path('collectionItems/<int:collection>/', get_collection,name='collection_Items'),
    path('FindKeyword/', FindKeyword,name='Find_Keyword'),
    path('DeleteCollection/<int:collectionId>/', DeleteCollection,name='DeleteCollection'),
    path('DeleteCollectionItem/<int:collectionItemId>/', DeleteCollectionItem,name='DeleteCollectionItem'),
    path('sendMail/', sendMail,name='sendMail'),
    # path('search_products/<int:page>/', Search_Discovery,name='search_products'),
]

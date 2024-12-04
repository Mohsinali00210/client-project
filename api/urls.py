# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getCommision,CollectionsSearchView,CollectionItemsSearchView,CollectionViewSet, CollectionItemsViewSet,CollectionCreateView,CollectionItemsCreateView

router = DefaultRouter()
router.register(r'Collections', CollectionViewSet)
router.register(r'Collectionitems', CollectionItemsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('CreateCollections/', CollectionCreateView.as_view(), name='collection-create'), 
    path('CreateCollection-items/', CollectionItemsCreateView.as_view(), name='collection-items-create'),
    path('Collection-items/search/', CollectionItemsSearchView.as_view(), name='collection-items-search'),
    path('Collection/search/', CollectionsSearchView.as_view(), name='collection-search'),
    path('getCommision', getCommision.as_view(), name='get-Commision'),
    path('getCommision2/', getCommision.as_view(), name='get_Commision2'),
]

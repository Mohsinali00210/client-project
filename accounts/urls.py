from .views import isUserLoggedIn,test_view,login_view, register_view,logout_view
from django.urls import path, include

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),  # Added home page URL
    path('test/', test_view, name='test'),  # Added home page URL
    path('fetchDetail/', isUserLoggedIn, name='fetchDetail'),  # Added home page URL
]

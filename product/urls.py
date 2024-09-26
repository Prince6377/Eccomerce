from django.urls import path
from .views import *

urlpatterns = [
    # path("<slug>/" , get_product , name='get_product'),
    path('product/<slug:slug>/', get_product, name='get_product'),
    
]

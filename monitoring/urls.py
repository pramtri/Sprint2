from django.contrib import admin
from django.urls import path, include
from inventory.views import health_check

urlpatterns = [
    path('', health_check),              
    path('', include('inventory.urls')),  
]

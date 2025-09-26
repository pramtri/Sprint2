from django.contrib import admin
from django.urls import path, include
from inventory.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check),              
    path('', include('inventory.urls')),  
]

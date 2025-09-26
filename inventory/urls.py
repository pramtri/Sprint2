from django.urls import path
from .views import availability, health_check

urlpatterns = [
    path("inventory/availability/", availability),
    path("health-check/", health_check),
]

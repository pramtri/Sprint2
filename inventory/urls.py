from django.urls import path
from .views import health_check, request_packaging

urlpatterns = [
    path("health-check/", health_check),
    path("orders/pack/", request_packaging), # NUEVO ENDPOINT
]
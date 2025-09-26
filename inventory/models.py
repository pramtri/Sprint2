from django.db import models

class Warehouse(models.Model):
    code = models.CharField(max_length=16, unique=True)

class Product(models.Model):
    sku = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    location = models.CharField(max_length=64, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="products")
    updated_at = models.DateTimeField(auto_now=True)

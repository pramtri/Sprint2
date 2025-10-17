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

# --- NUEVO MODELO ---
class Order(models.Model):
    STATUS_CHOICES = [
        ('verified', 'Verificado'),
        ('packing', 'Empacando'),
        ('packed', 'Empacado por despachar'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Usamos un ID único para referenciar el pedido fácilmente
    order_id = models.CharField(max_length=64, unique=True, db_index=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='verified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"
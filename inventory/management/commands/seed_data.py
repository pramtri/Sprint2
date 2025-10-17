from django.core.management.base import BaseCommand
from inventory.models import Product, Warehouse, Order
import random
import uuid

class Command(BaseCommand):
    help = "Seed products and orders into the database"

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=10000)
        parser.add_argument("--orders", type=int, default=500) # Pedidos para la prueba

    def handle(self, *args, **options):
        num_products = options["products"]
        num_orders = options["orders"]

        # --- Crear Bodega y Productos ---
        self.stdout.write("Seeding products...")
        w, _ = Warehouse.objects.get_or_create(code="BOD-001")
        products_to_create = []
        for i in range(num_products):
            products_to_create.append(Product(
                sku=f"SKU{str(i).zfill(6)}",
                name=f"Producto {i}",
                stock=random.randint(10, 100),
                location=f"A-{random.randint(1, 200)}",
                warehouse=w
            ))
        Product.objects.bulk_create(products_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {num_products} products"))

        # --- Crear Pedidos en estado 'verified' ---
        self.stdout.write("Seeding orders...")
        product_ids = list(Product.objects.values_list('id', flat=True))
        if not product_ids:
            self.stdout.write(self.style.ERROR("No products found to create orders. Seed products first."))
            return
            
        orders_to_create = []
        order_ids_for_csv = []
        for i in range(num_orders):
            order_id_str = str(uuid.uuid4())
            orders_to_create.append(Order(
                product_id=random.choice(product_ids),
                order_id=order_id_str,
                status='verified'
            ))
            order_ids_for_csv.append(order_id_str)
            
        Order.objects.bulk_create(orders_to_create, ignore_conflicts=True)

        # --- Guardar los IDs de los pedidos en un CSV para JMeter ---
        with open("order_ids.csv", "w") as f:
            for order_id in order_ids_for_csv:
                f.write(f"{order_id}\n")
        
        self.stdout.write(self.style.SUCCESS(f"Seeded {num_orders} orders and created order_ids.csv"))
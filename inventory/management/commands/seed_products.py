from django.core.management.base import BaseCommand
from inventory.models import Product, Warehouse
import random

class Command(BaseCommand):
    help = "Seed N products into the database"

    def add_arguments(self, parser):
        parser.add_argument("--n", type=int, default=100000)

    def handle(self, *args, **options):
        n = options["n"]
        w, _ = Warehouse.objects.get_or_create(code="BOD-001")

        batch = []
        for i in range(n):
            batch.append(Product(
                sku=f"SKU{str(i).zfill(6)}",
                name=f"Producto {i}",
                stock=random.randint(0, 50),
                location=f"A-{random.randint(1, 200)}",
                warehouse=w
            ))

            if len(batch) >= 5000:  # inserciones por lotes
                Product.objects.bulk_create(batch, ignore_conflicts=True)
                batch.clear()

        if batch:
            Product.objects.bulk_create(batch, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Seeded {n} products"))

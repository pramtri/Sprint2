from django.core.management.base import BaseCommand
from inventory.models import Product, Warehouse
import random, string

def rnd_sku(i): return f"SKU{str(i).zfill(6)}"

class Command(BaseCommand):
    help = "Seed 100k products"

    def add_arguments(self, parser):
        parser.add_argument("--n", type=int, default=100000)

    def handle(self, *args, **opts):
        n = opts["n"]
        w,_ = Warehouse.objects.get_or_create(code="BOD-001")
        batch = []
        for i in range(n):
            batch.append(Product(
                sku=rnd_sku(i),
                name=f"Producto {i}",
                stock=random.randint(0, 50),
                location="A-{0}".format(random.randint(1, 200)),
                warehouse=w
            ))
            if len(batch) >= 5000:
                Product.objects.bulk_create(batch, ignore_conflicts=True)
                batch.clear()
        if batch:
            Product.objects.bulk_create(batch, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} products"))

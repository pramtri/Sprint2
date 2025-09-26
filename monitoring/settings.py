DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "inventorydb",
        "USER": "inventory",
        "PASSWORD": "your-strong-pass",
        "HOST": "DB_PRIVATE_IP",  # cámbiala por la IP privada de la EC2 de la DB
        "PORT": "5432",
    }
}
ALLOWED_HOSTS = ["*",]  # para pruebas

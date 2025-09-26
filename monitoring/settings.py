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

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
]
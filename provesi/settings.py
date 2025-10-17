DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "provesi_db",
        "USER": "provesi_user",
        "PASSWORD": "isis2503",
        "HOST": "provesi-db.c1ikg4aowpxo.us-east-1.rds.amazonaws.com",
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

ROOT_URLCONF = 'provesi.urls'

WSGI_APPLICATION = 'provesi.wsgi.application'
ALLOWED_HOSTS = ['*']
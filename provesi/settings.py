DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "provesi_db",
        "USER": "provesi_user",
        "PASSWORD": "isis2503",
        "HOST": "172.31.29.123",
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
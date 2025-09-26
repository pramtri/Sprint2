DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "monitoring_db",
        "USER": "monitoring_user",
        "PASSWORD": "isis2503",
        "HOST": "172.31.29.123",
        "PORT": "5432",
    }
}
ALLOWED_HOSTS = ["*",]  # para pruebas

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
]

ROOT_URLCONF = 'monitoring.urls'

WSGI_APPLICATION = 'monitoring.wsgi.application'
ALLOWED_HOSTS = ['*']
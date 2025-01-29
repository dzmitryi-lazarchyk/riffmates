from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodmates',
        'USER': 'postgres',
        'PASSWORD': 'admin',
    }
}
from ryshop.settings import *
SECRET_KEY = 'd(8d$%%#!umoqd!ssnxdh+7^jf(kc0_5elct%6#gogx7yi%t-*'

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ryshop',
        'USER': 'postgres',
        'PASSWORD': "postgres",
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

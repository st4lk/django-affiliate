from settings import *

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = '!!!change_me!!!'

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

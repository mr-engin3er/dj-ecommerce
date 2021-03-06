from .base import *

DEBUG = False

# TODO: add site ip and url
ALLOWED_HOSTS = ['ip-address', 'www.domain.com']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# TODO: configure database connectivity
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# TODO: Setup email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'some url like AWS S3'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'), ]

MEDIA_URL = 'some url like AWS S3'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

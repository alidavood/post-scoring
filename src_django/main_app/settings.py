from pathlib import Path

import environ

#################
# Load env region
#################
env = environ.Env()

######################
# Basic config region
######################
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
ROOT_URLCONF = 'main_app.urls'
API_V1_PREFIX = env.str('API_V1_PREFIX')
AUTH_USER_MODEL = 'user.User'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
TEST_MODE = False  # Automatically will set to `True` when you run a test
TEST_RUNNER = 'seedwork.utils.CustomTestRunner'

#############
# Apps region
#############
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
EXTERNAL_APPS = [
    'rest_framework',
    'drf_yasg',
]
INTERNAL_APPS = [
    'apps.user',
    'apps.blog',
]
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + INTERNAL_APPS

###################
# Middleware region
###################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##################
# Templates region
##################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#################
# DataBase region
#################
DATABASES = {'default': env.db()}

##############
# Cache region
##############
CACHES = {'default': env.cache()}

########################
# Password Policy region
########################
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

#############################
# Internationalization region
#############################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

###############
# Static region
###############
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

##############
# Media region
##############
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

####################
# WSGI config region
####################
WSGI_APPLICATION = 'main_app.wsgi.application'

############
# DRF region
############
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

#########
# Swagger
#########
SWAGGER_SETTINGS = {
    # 'DEFAULT_AUTO_SCHEMA_CLASS': 'utils.swagger.CompoundTagsSchema',
    # 'DEFAULT_INFO': 'main_app.urls.api_info',
}

################
# Logging region
################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}\n',
            'style': '{'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'suds': {
            'handlers': [],
            'propagate': True,
            'level': 'CRITICAL',
        },
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

###################
# Auth
###################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

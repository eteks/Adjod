# Django settings for adjod project.
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.conf.urls import patterns, include, url
import smtplib
from django.utils.translation import ugettext_lazy, ugettext as _
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ('admin', ''),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'adjod',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Singapore'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
LANGUAGE_COOKIE_NAME = 'adjod_language' 

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LANGUAGES = (('ms', _('Malay')), 
             ('zh', _('Chinese')),              
             ('en', _('English')), 
            ) 

ugettext = lambda s: s 

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

# STATIC_ROOT = '/static_files/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

SITE_NAME = '52.34.51.104'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'static'),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i95gwsqfo9nmejbll=t@!3z1(2@l4#9hee7!3x6dw8ad^&amp;u*cb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
 # setting for social auth backend  and tracking by Priya
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'adjod.middleware.Global',
    'tracking.middleware.VisitorTrackingMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
)

# settings for social auth redirect for home by priya
TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
     'django.core.context_processors.i18n',
     'django.core.context_processors.csrf',
     'django.core.context_processors.media',
     'django.core.context_processors.static',
     'django.core.context_processors.debug',
     'adjod.context_processors.global_activity',
     'social_auth.context_processors.social_auth_by_name_backends',
     'social_auth.context_processors.social_auth_backends',
     'social_auth.context_processors.social_auth_by_type_backends',
     'social_auth.context_processors.social_auth_login_redirect',
)

#set the Language tranlation path for accessing .po file
LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '../locale'),
)

USE_I18N = True

ROOT_URLCONF = 'adjod.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'adjod.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Apps
    'adjod',
    'advertisement',
    'search',
    'worker',
    'banner',
    'chat',
    'commerce',
    'logs',
    'tracking',

    # Third Party Libs
    'haystack',
    'paypal.standard.ipn',
    'djmoney_rates',
    'social_auth',
    'tracking'
    # 'communication',
    # 'smsverify',
    # 'rollyourown.seo',
    # 'django_nose',

)

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# PAYPAL_RECEIVER_EMAIL = "kalaimca.gs-facilitator@gmail.com"
# PAYPAL_TEST = True
# PAYPAL_WPP_USER="kalaimca.gs-facilitator_api1.gmail.com"
# PAYPAL_WPP_PASSWORD="E5K4SG8QVGCDNHCB"
# PAYPAL_WPP_SIGNATURE="An5ns1Kso7MWUdW4ErQKJJJ4qi4-AGHrwon-aVUnmGFr91HclSLKbD9i"
# # PAYPAL_NOTIFY_URL = "URL_ROOT/charge/difficult_to_guess"
# # PAYPAL_RETURN_URL = "URL_ROOT/charge/return/"
# # PAYPAL_CANCEL_URL = "URL_ROOT/charge/cancel/"
# # PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
# # PAYPAL_BUSS_EMAIL = 'kalaimca.gs@gmail.com'
# SANDBOX_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
# SANDBOX_BUSS_EMAIL = 'kalaimca.gs@gmail.com'

PAYPAL_TEST = True

# PAYPAL_RECEIVER_EMAIL = "deepakkuppusamy.gs@gmail.com"
PAYPAL_RECEIVER_EMAIL = "kalairkv.mca14-facilitator@gmail.com"

#Sandbox url For testing
SANDBOX_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
SANDBOX_BUSS_EMAIL = 'kalairkv.mca14-facilitator@gmail.com'

#Paypal URL for Live
# PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
# PAYPAL_BUSS_EMAIL = 'kalaimca.gs@gmail.com'

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = dict(
  default = dict(
    ENGINE = 'search.searchsites.AdjodSearchEngine',
    # URL = 'http://46.4.81.207:9200/',
    URL = 'http://127.0.0.1:9200/',
    INDEX_NAME = 'adjod',
    # TIMEOUT = '60'
  )
)

HAYSTACK_CUSTOM_HIGHLIGHTER ='adjod.search_sites.SearchHighlighter'

# SEARCH_PAGE_NUMBER_OF_LEADS = 70

# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGIN_ERROR_URL = '/login_error/'

AUTHENTICATION_BACKENDS = (
    # setting for authenticate facebook and gmail login by priya
    'django.contrib.auth.backends.ModelBackend',
    #'django.contrib.auth.models.AnonymousUser ',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',

)

# settings for storing logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'resell.log',
            'formatter': 'verbose'
        },
        'db':{
            'level': 'WARNING',
            'class': 'logs.loggers.MyDbLogHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['db', 'file'],
            'level': 'WARNING',
            'propagate': False,
            },
        'myapplog': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
            }
        }
}

# settings for SMS verification
TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TWILIO_AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

AUTH_PROFILE_MODULE = 'adjod.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 1

# settings for Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testmail123sample@gmail.com'
#old
# EMAIL_HOST_PASSWORD = 'testmail123'
#new
EMAIL_HOST_PASSWORD = 'testsample'
EMAIL_PORT = 587

SEO_MODEL_REGISTRY = (
    ('test_project.MyMetadata', ('template_test', )),
)

# settings for GEO (comment for future reference)
# GEOIP_PATH = os.path.join(os.path.dirname(__file__), 'static/geoip/')

# settings for Currency Conversion
DJANGO_MONEY_RATES = {
                'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
                'OPENEXCHANGE_URL': 'http://openexchangerates.org/api/latest.json',
                'OPENEXCHANGE_APP_ID': 'd4260d5caac9454996445fd14eb58591',
                'OPENEXCHANGE_BASE_CURRENCY': 'USD',
}
CURRENCY_RATES = 'USD'

BASE_CURRENCY = 'SGD'

# setting for facebook login and gmail login by priya
LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'
AUTH_USER_EMAIL_UNIQUE = True

# Api key for Facebook login
FACEBOOK_APP_ID='1049305695115171'
FACEBOOK_API_SECRET='8a4ff3b263cba30038b815390975cede'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'pl_PL',
  'fields': 'id, name, email',
}

# Api key for gmail login
GOOGLE_OAUTH2_CLIENT_ID='625095837948-e5rsdpqdcr7vmu8fb6krnru7vvu5iqgq.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET ='1wfBaMwN2KaEA-xyd3C582ix'
GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_USER_MODEL = 'auth.User'
GOOGLE_OAUTH2_USE_DEPRECATED_API = True

SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'

SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TRACK_PAGEVIEWS = True

SOCIAL_AUTH_PIPELINE = (
'social_auth.backends.pipeline.social.social_auth_user',
'social_auth.backends.pipeline.associate.associate_by_email',
'social_auth.backends.pipeline.user.get_username',
'social_auth.backends.pipeline.user.create_user',
'social_auth.backends.pipeline.social.associate_user',
'social_auth.backends.pipeline.user.update_user_details',

)

PAYPAL_DICT = {
    'cancel_return' : '/postad/',
    'success_return': '/paypal/',
    'notify_url'    : '/paypal/'
}
#setting for send mail template subject
TEMPLATED_EMAIL_DJANGO_SUBJECTS = {
    'welcome':'Welcome to Resell',
    'post_ad':'Thanks for sharing your ads with Resell',
    'alert'  :'Matching Ads',
    'product_alert':'Remainder Mail for your Product',
}
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

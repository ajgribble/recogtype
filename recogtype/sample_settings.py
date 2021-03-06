# Django settings for recogtype project.

import os.path
import posixpath
import socket

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if socket.gethostname() == '':
    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = {
                                'INTERCEPT_REDIRECTS': False,
                           }
    # Additional locations of static files
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".   
        '/home/grib/PythonProjects/recogtype/recogtype/static/',
    )
else:
    DEBUG = False
    DEFAULT_FROM_EMAIL = 'debug@recogtype.com'
    SERVER_EMAIL = 'error@recogtype.com'
    STATICFILES_DIRS = (
            # Put strings here, like "/home/html/static" or "C:/www/django/static".   
            '/home/ajgribble/webapps/django/recogtype/recogtype/static/',
    )

TEMPLATE_DEBUG = DEBUG
ADMINS = (
    (''),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qm1ef-+$a1x#@zrf!aclhvl64-og0x%wd6ovtm!0jn*^48_1-5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Settings used by Guardian
ANONYMOUS_USER_ID = -1

# Settings used by Userena
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
USERENA_DEFAULT_PRIVACY = 'closed'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_WITHOUT_USERNAMES = True
USERENA_HIDE_EMAIL = True
USERENA_SIGNIN_REDIRECT_URL = '/dashboard/%(username)s/'
USERENA_ACTIVATION_REQUIRED = False

# Settings used by Django-Debug-Toolbar
INTERNAL_IPS = ('127.0.0.1',)

# Settings used by Django
AUTH_PROFILE_MODULE = 'profiles.Profile'
LOGIN_URL = '/signin'
LOGOUT_URL = '/signout'
LOGIN_REDIRECT_URL = '/profiles/%(username)s/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'recogtype.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'recogtype.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates")
)

INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',

    # Third Party Apps
    'userena',
    'guardian',
    'easy_thumbnails',
    'south',
    'debug_toolbar',
    'django_countries',

    # Project Specific Apps
    'profiles',
    'recogmatch',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

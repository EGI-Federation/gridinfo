from ConfigParser import RawConfigParser, NoSectionError
from django.core.exceptions import ImproperlyConfigured

# Django settings for wlcg project.

PROJECT_NAME = 'gstat'

# Set up some useful paths for later
from os import path as os_path
APP_PATH = os_path.abspath(os_path.split(__file__)[0])
PROJECT_PATH = os_path.abspath(os_path.join(APP_PATH,'..','..'))
config = RawConfigParser()
config_file=os_path.join(PROJECT_PATH, 'config', '%s.ini'%PROJECT_NAME)
read_files = config.read(['/etc/gstat/gstat.ini',config_file])

#$ this seems to mask underlyinh errors, and we'll catch them in the next line !
#if not read_files:
#raise ImproperlyConfigured("Could not read config file : %s"%config_file)

try:
    DEBUG = config.getboolean('debug','DEBUG')
    TEMPLATE_DEBUG = config.getboolean('debug','TEMPLATE_DEBUG')

    PREFIX = config.get('server', 'PREFIX')
    REFERENCE_BDII_FILE = config.get('server', 'REFERENCE_BDII_FILE')
    
    NAGIOS_STATUS_FILE = config.get('nagios', 'NAGIOS_STATUS_FILE')

    VIEW_TEST = config.getboolean('debug', 'VIEW_TEST')
    INTERNAL_IPS = tuple(config.get('debug', 'INTERNAL_IPS').split())

    SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
    EMAIL_HOST = config.get('email', 'EMAIL_HOST')
    ADMINS = tuple(config.items('error mail'))
    MANAGERS = tuple(config.items('404 mail'))

    
    DATABASE_USER = config.get('database', 'DATABASE_USER')
    DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
    DATABASE_HOST = config.get('database', 'DATABASE_HOST')
    DATABASE_PORT = config.get('database', 'DATABASE_PORT')
    DATABASE_ENGINE = config.get('database', 'DATABASE_ENGINE')
    DATABASE_NAME = config.get('database', 'DATABASE_NAME')
    TEST_DATABASE_NAME = config.get('database', 'TESTSUITE_DATABASE_NAME')


    # Make these unique, and don't share it with anybody.
    SECRET_KEY = config.get('secrets','SECRET_KEY')
    CSRF_MIDDLEWARE_SECRET = config.get('secrets', 'CSRF_MIDDLEWARE_SECRET')
except NoSectionError, e:
    raise ImproperlyConfigured(e)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if DEBUG:
    MEDIA_ROOT = os_path.join(PROJECT_PATH,'/media')
else:
    MEDIA_ROOT = ''
    
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if PREFIX != '':
    ADMIN_MEDIA_PREFIX = '/%s/admin/media/'%PREFIX
else:
    ADMIN_MEDIA_PREFIX ='/admin/media/' 

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'core.urls'

TEMPLATE_DIRS = (
    os_path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'core',
    'geo',    
    'glue',
    'gridmap',
    'gridsite',
    'ldapbrowser',
    'rrd',
    'service',
    'summary',
    'topology',
    'vo',
#    'debug_toolbar',
)

# Various apps available

# Django settings file for a project based on the playdoh template.

from funfactory.settings_base import *

from django_sha2 import get_password_hashers
PASSWORD_HASHERS = get_password_hashers(BASE_PASSWORD_HASHERS, HMAC_KEYS)

INSTALLED_APPS = get_apps(append=(
    'dragnet.users',
    'dragnet.dll',
    
))

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'debug_toolbar',
]

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))

AUTH_PROFILE_MODULE = 'users.UserProfile'
LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

try:
    ## LDAP
    import ldap

    AUTHENTICATION_BACKENDS = (
       'dragnet.users.email_auth_backend.EmailOrUsernameModelBackend',
       'dragnet.users.auth.backends.MozillaLDAPBackend',
       'django.contrib.auth.backends.ModelBackend',
    )

    # these must be set in settings/local.py!
    AUTH_LDAP_SERVER_URI = ''
    AUTH_LDAP_BIND_DN = ''
    AUTH_LDAP_BIND_PASSWORD = ''

    AUTH_LDAP_START_TLS = True
    AUTH_LDAP_USER_ATTR_MAP = {
      "first_name": "givenName",
      "last_name": "sn",
      "email": "mail",
    }
    from django_auth_ldap.config import LDAPSearch
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
      "dc=mozilla",
      ldap.SCOPE_SUBTREE,
      "mail=%(user)s"
    )

except ImportError:
    AUTHENTICATION_BACKENDS = (
       'dragnet.users.email_auth_backend.EmailOrUsernameModelBackend',
       'django.contrib.auth.backends.ModelBackend',
    )

ROOT_URLCONF = 'dragnet.urls'

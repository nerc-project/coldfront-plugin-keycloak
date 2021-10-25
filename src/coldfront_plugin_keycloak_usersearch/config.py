from coldfront.config.base import INSTALLED_APPS
from coldfront.config.env import ENV

KEYCLOAK_URL = ENV.get_value('KEYCLOAK_URL')
KEYCLOAK_USER = ENV.get_value('KEYCLOAK_USER')
KEYCLOAK_PASS = ENV.get_value('KEYCLOAK_PASS')
KEYCLOAK_REALM = ENV.get_value('KEYCLOAK_REALM')

if 'coldfront_plugin_keycloak_usersearch' not in INSTALLED_APPS:
    INSTALLED_APPS += [
        'coldfront_plugin_keycloak_usersearch',
    ]

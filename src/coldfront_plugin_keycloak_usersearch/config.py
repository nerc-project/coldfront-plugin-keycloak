from coldfront.config.base import INSTALLED_APPS
from coldfront.config.env import ENV

if 'coldfront_plugin_keycloak_usersearch' not in INSTALLED_APPS:
    INSTALLED_APPS += [
        'coldfront_plugin_keycloak_usersearch',
    ]

from coldfront.core.user.utils import UserSearch
from coldfront.core.utils.common import import_from_settings
from coldfront.config.env import ENV

from coldfront_plugin_keycloak_usersearch.keycloak import KeycloakClient

KEYCLOAK_URL = ENV.get_value('KEYCLOAK_URL')
KEYCLOAK_USER = ENV.get_value('KEYCLOAK_USER')
KEYCLOAK_PASS = ENV.get_value('KEYCLOAK_PASS')
KEYCLOAK_REALM = ENV.get_value('KEYCLOAK_REALM')

KEYCLOAK_CLIENT = None  # type: KeycloakClient


class KeycloakUserSearch(UserSearch):
    search_source = 'keycloak'

    def __init__(self, *args, **kwargs):
        global KEYCLOAK_CLIENT
        if not KEYCLOAK_CLIENT:
            KEYCLOAK_CLIENT = KeycloakClient(KEYCLOAK_URL,
                                             KEYCLOAK_USER,
                                             KEYCLOAK_PASS)

        super().__init__(*args, **kwargs)

    def search_a_user(self, user_search_string=None, search_by='all_fields'):
        # search_by is in ['all_fields', 'username_only']

        matches = KEYCLOAK_CLIENT.search_username(user_search_string, KEYCLOAK_REALM)
        # Filter out all the internal values before passing on the result
        # since username is all that's parsed
        # https://github.com/ubccr/coldfront/blob/9e49edd3f37bc32548b3408ea0ff55e03f7369cb/coldfront/core/user/utils.py#L96
        return [{'username': match['username']} for match in matches]

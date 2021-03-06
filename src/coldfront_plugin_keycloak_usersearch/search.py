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

        if search_by == 'all_fields':
            matches = KEYCLOAK_CLIENT.search(user_search_string, KEYCLOAK_REALM)
        elif search_by == 'username_only':
            matches = KEYCLOAK_CLIENT.search_username(user_search_string, KEYCLOAK_REALM)
        else:
            raise ValueError('search_by must be one of all_fields, username_only')

        # Filter out all the internal values before passing on the result
        return [
            {
                'username': match['username'],
                'last_name': match.get('lastName', ''),
                'first_name': match.get('firstName', ''),
                'email': match.get('email', ''),
                'source': self.search_source,
            }
            for match in matches
        ]

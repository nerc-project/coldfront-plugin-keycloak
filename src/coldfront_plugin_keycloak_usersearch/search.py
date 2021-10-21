from coldfront.core.user.utils import UserSearch
from coldfront.core.utils.common import import_from_settings


class KeycloakUserSearch(UserSearch):
    search_source = 'keycloak'

    def search_a_user(self, user_search_string=None, search_by='all_fields'):
        pass

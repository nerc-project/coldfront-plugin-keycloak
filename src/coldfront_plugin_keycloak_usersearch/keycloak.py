import requests


class KeycloakClient(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        self.session = requests.session()
        self._admin_auth()

    def construct_url(self, realm, path):
        return f'{self.url}/auth/admin/realms/{realm}/{path}'

    @property
    def url_base(self):
        return f'{self.url}/auth/admin/realms'

    def auth_endpoint(self, realm):
        return f'{self.url}/auth/realms/{realm}/protocol/openid-connect/auth'

    def token_endpoint(self, realm):
        return f'{self.url}/auth/realms/{realm}/protocol/openid-connect/token'

    def _admin_auth(self):
        params = {
            'grant_type': 'password',
            'client_id': 'admin-cli',
            'username': self.username,
            'password': self.password,
            'scope': 'openid',
        }
        r = requests.post(self.token_endpoint('master'), data=params).json()
        headers = {
            'Authorization': ("Bearer %s" % r['access_token']),
            'Content-Type': 'application/json'
        }
        self.session.headers.update(headers)
        return r

    def search_username(self, username, realm):
        self._admin_auth()
        return self.session.get(self.construct_url(
            realm, f'users?username={username}')).json()

    def search(self, value, realm):
        self._admin_auth()
        return self.session.get(self.construct_url(
            realm, f'users?search={value}')).json()

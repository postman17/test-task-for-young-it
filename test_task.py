import requests


URL_AUTH = 'https://{}.amocrm.ru/private/api/auth.php?type=json'
URL_ACCOUNT = 'https://{}.amocrm.ru/api/v2/account'
URL_INCOMING_LEADS = 'https://{}.amocrm.ru/api/v2/account'


class AmoCrmApi:
    def __init__(self, login, user_email, user_hash):
        self.login = login
        self.user_email = user_email
        self.user_hash = user_hash

    def _send_get_request(self, url, params, cookies):
        return requests.get(url, params=params, cookies=cookies)

    def _auth(self):
        json = {
            'USER_LOGIN': self.user_email,
            'USER_HASH': self.user_hash
        }
        url = URL_AUTH.format(self.login)
        response = requests.post(url, json=json)
        if response.status_code != 200:
            return
        return response.cookies.get_dict()

    def account(self):
        cookies = self._auth()
        if not cookies:
            return 'Authorization error'
        params = {
            'with': ['pipelines', 'groups', 'note_types', 'task_types']
        }
        url = URL_ACCOUNT.format(self.login)
        response = self._send_get_request(url, params, cookies)
        return response.json()

    def incoming_leads(self, page_size, page, categories):
        cookies = self._auth()
        if not cookies:
            return 'Authorization error'
        params = {
            'page_size': page_size,
            'page': page,
            'categories': categories
        }
        url = URL_INCOMING_LEADS.format(self.login)
        response = self._send_get_request(url, params, cookies)
        return response.json()

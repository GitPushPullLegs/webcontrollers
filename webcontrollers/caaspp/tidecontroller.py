from .caasppbasecontroller import CAASPPBaseController
import requests
import json
from urllib.parse import quote


class TIDEController(CAASPPBaseController):
    _HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    def login(self, username: str, password: str, retrieve_login_code=None, **kwargs):
        """
        Logs into CERS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self._login(link="https://ca.tide.cambiumast.com/",
                    username=username, password=password, retrieve_login_code=retrieve_login_code, **kwargs)
        self._get_impersonate_dto()

    def _setup_request_session(self):
        session = requests.session()
        session.headers.update(self._HEADERS)
        [session.cookies.set(c['name'], c['value']) for c in self.driver.get_cookies()]
        return session

    def _get_impersonate_dto(self):
        session = self._setup_request_session()
        data = json.loads(session.post(r"https://ca.tide.cambiumast.com/api/Authorization/GetImpersonateDTO").text)
        client_name = data['ClientList'][0]['Code']
        test_administration_key = data['TestAdministrationsList'][0]['Code']
        roles = []
        for role in data['RolesList']:
            if role['DataProperty'] == 'DISTRICT':
                roles.append({'title': role['Label'], 'code': role['Code']})
        self.client_name = client_name
        self.test_administration_key = test_administration_key
        print(roles)

        #TODO: Use this to set the role of the user.
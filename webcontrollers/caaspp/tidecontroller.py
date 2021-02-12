from .caasppbasecontroller import CAASPPBaseController
import requests
import json


class TIDEController(CAASPPBaseController):

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

    def _get_impersonate_dto(self):
        _HEADERS = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        session = requests.session()
        session.headers.update(_HEADERS)
        [session.cookies.set(c['name'], c['value']) for c in self.driver.get_cookies()]
        data = session.post(r"https://ca.tide.cambiumast.com/api/Authorization/GetImpersonateDTO").text
        #TODO: Use this to set the role of the user.
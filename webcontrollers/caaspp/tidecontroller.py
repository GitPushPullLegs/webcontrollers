from webcontrollers.common import WebController


class TIDEController(WebController):

    def login(self, username: str, password: str, retrieve_login_code=None, **kwargs):
        """
        Logs into CERS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self._login(link="https://ca.tide.cambiumast.com/",
                    username=username, password=password, retrieve_login_code=retrieve_login_code, **kwargs)
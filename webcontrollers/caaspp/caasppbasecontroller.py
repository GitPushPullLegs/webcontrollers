from selenium.common.exceptions import *

from webcontrollers.common import WebController
from webcontrollers.common.errors import *


class CAASPPBaseController(WebController):

    def _login(self, link: str, username: str, password: str, retrieve_login_code=None, **kwargs):
        """
        Logs into TOMS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self.driver.get(link)
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="kc-login"]').click()
        try:
            if self.driver.find_element_by_xpath('//*[text()="The username or password you entered is incorrect. To '
                                                 'request a new link for resetting your password, select "]'):
                raise AuthenticationError('Invalid credentials.')
        except NoSuchElementException:
            pass

        if self.driver.find_elements_by_id('emailcode'):
            if not retrieve_login_code:
                raise AuthenticationError('Missing login code function.')

            email_code = retrieve_login_code(**kwargs)
            self.driver.find_element_by_id('emailcode').send_keys(email_code)
            self.driver.find_element_by_id('kc-login').click()

        try:
            if self.driver.find_element_by_xpath('//*[text()="Invalid email code. Please try again"]'):
                raise AuthenticationError('Invalid login code.')
        except NoSuchElementException:
            pass
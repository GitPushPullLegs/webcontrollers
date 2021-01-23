from webcontrollers.common import WebController
from selenium.common.exceptions import *
from webcontrollers.common.errors import *
from wait import BrowserWait


class SEISController(WebController):

    def login(self, username: str, password: str):
        self.driver.get('https://seis.org/login')
        BrowserWait(browser=self.driver).until_angular_loads()

        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/div/button').click()
        BrowserWait(browser=self.driver).until_angular_loads()

        try:
            if self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div'):
                raise AuthenticationError("Username or password incorrect.")
        except NoSuchElementException as exc:
            pass
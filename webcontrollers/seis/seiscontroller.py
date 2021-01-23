from webcontrollers.common import WebController
from selenium.common.exceptions import *
from webcontrollers.common.errors import *
from wait import BrowserWait, Wait
from datetime import datetime, timedelta
import dateutil.parser

class SEISController(WebController):

    def login(self, username: str, password: str):
        """
        Logs into SEIS.
        :param username:
        :param password:
        """
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

    def _download_report(self):
        """Initiates the download of a report and returns the file path of the download."""
        requested_time = datetime.now() - timedelta(seconds=3)
        self.driver.find_element_by_xpath('//*[@id="form"]/div/div/div/div/div[1]/div/div/button').click()
        Wait().until(self._report_ready, requested_time=requested_time)

        self.driver.find_elements_by_xpath('//*[text()="XLSX"]')[1].click()
        BrowserWait(browser=self.driver).until_angular_loads()

        return BrowserWait(browser=self.driver).until_file_downloaded()

    def _report_ready(self, requested_time):
        """Checks if the latest report came after the request."""
        elements = self.driver.find_elements_by_tag_name('td')
        latest_report_time = dateutil.parser.parse(elements[6].text)
        if latest_report_time > requested_time:
            return True

    def download_toms_summative_report(self):
        """Downloads the TOMS Summative Test Settings Report and returns the file path."""
        self.driver.get('https://seis.org/reports/toms')
        BrowserWait(browser=self.driver).until_angular_loads()
        return self._download_report()

    def download_toms_interim_report(self):
        """Downloads the TOMS Interim Test Settings Report and returns the file path."""
        self.driver.get('https://seis.org/reports/tomsinterim')
        BrowserWait(browser=self.driver).until_angular_loads()
        return self._download_report()
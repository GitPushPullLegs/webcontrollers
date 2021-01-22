from webcontrollers.common.webcontroller import WebController
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webcontrollers.common.errors import *


class CERSController(WebController):

    def login(self, username: str, password: str, retrieve_login_code=None):
        """
        Logs into CERS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self.driver.get(
            "https://login.smarterbalanced.org/sso/saml2/0oa14zrzacExSAFK5357?fromURI=https://login.smarterbalanced.org/home/smarterbalancedassessmentconsortium_cersproduction_1/0oa17s5opaczfbT05357/aln17sbcwtNiV39Uq357")
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="kc-login"]').click()

        try:
            if self.driver.find_element_by_xpath('//*[text()="The username or password you entered is incorrect. To '
                                                 'request a new link for resetting your password, select "]'):
                raise AuthenticationError('Username or password incorrect.')
        except NoSuchElementException:
            pass

        if self.driver.find_elements_by_id('emailcode'):
            if not retrieve_login_code:
                raise AuthenticationError('Missing login code function.')

            email_code = retrieve_login_code()
            self.driver.find_element_by_id('emailcode').send_keys(email_code)
            self.driver.find_element_by_xpath('//*[@id="kc-login"]').click()

    def upload_groups(self, files: [str]):
        """Uploads student groups to CERS."""
        self.driver.get("https://reporting.smarterbalanced.org/admin-groups/import")

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/admin/div[1]/div[3]'))
            )
        except:
            print("Error")

        self.driver.execute_script(
            f"""document.evaluate('//*[@id="maincontent"]/admin/div[1]/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute("hidden")""")

        file_upload = self.driver.find_element_by_xpath('//*[@id="maincontent"]/admin/div[1]/div[3]/input')
        [file_upload.send_keys(file) for file in files]

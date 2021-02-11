from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .caasppbasecontroller import CAASPPBaseController


class CERSController(CAASPPBaseController):

    def login(self, username: str, password: str, retrieve_login_code=None, **kwargs):
        """
        Logs into CERS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self._login(link="https://login.smarterbalanced.org/sso/saml2/0oa14zrzacExSAFK5357?fromURI=https://login.smarterbalanced.org/home/smarterbalancedassessmentconsortium_cersproduction_1/0oa17s5opaczfbT05357/aln17sbcwtNiV39Uq357",
                    username=username, password=password, retrieve_login_code=retrieve_login_code, **kwargs)

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

import json
import re

from selenium.common.exceptions import *

from webcontrollers.common import WebController
from webcontrollers.common.errors import *
from wait import BrowserWait
from urllib.parse import urlsplit, urljoin


class TOMSController(WebController):

    def login(self, username: str, password: str, retrieve_login_code=None):
        """
        Logs into TOMS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self.driver.get('https://mytoms.ets.org')
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
            self.driver.find_element_by_xpath('//*[text()="Submit"]').click()

        self._gather_user_info()

    def _gather_user_info(self):
        """Pulls the user info and role info from the source code."""
        source = self.driver.page_source
        caaspp_info = json.loads(
            re.findall(r"(?<=var caasppInfoString = '){[A-Za-z0-9\\\" :,_{}\[\].@-]+}(?=')", source)[0].replace("\\t",
                                                                                                                "").replace(
                "\\", ""))
        self.username = caaspp_info['info']['userInfo']['username']
        self.user_id = caaspp_info['info']['userInfo']['user_id']

        self.roles = caaspp_info['info']['roleOrgs']

    def export_user_roles_to_csv(self, outfile_path):
        """
        Convenience function to export the user roles to a csv file.
        :param outfile_path: The file to be created, must end in .csv.
        """
        if not outfile_path.endswith(".csv"):
            raise AttributeError("outfile_path must end with .csv.")

        import \
            csv  # This function is for convenience, it will not be used often and we don't need to import csv for the rest of the module.

        with open(outfile_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            header = True
            for role in self.roles:
                if header:
                    csv_writer.writerow(role.keys())
                    header = False
                csv_writer.writerow(role.values())

    def set_role(self, organization_id: int, role_id: int):
        """
        Sets the role of the user in TOMS.

        If you don't know your organization id or role, execute the export_user_roles_to_csv method."""
        found_role = False
        for role in self.roles:
            if (role['role_id'] == role_id) & (role['org_id'] == organization_id):
                found_role = True

        if not found_role:
            raise KeyError(f"You do not have access to role: {role_id} for organization: {organization_id}."
                           f"If you do not know this information, execute the export_user_roles_to_csv method.")

        url_parts = [
            r'https://mytoms.ets.org/TOMS?selectedProgram=CAASPP',
            f'selectedRoleId={role_id}',
            f'selectedOrgId={organization_id}',
            'selectedAYC=6',
            'selectedExtended=0',
            f'username={self.username.replace("@", "%40")}',
            f'userid={self.user_id}'
        ]

        self.driver.get('&'.join(str(part) for part in url_parts))

    def download_test_settings_template(self) -> str:
        """Downloads the TOMS test settings file and returns the file path."""
        file_name = 'CAASPP_Upload_Stu_Accom_Template_2020-2021_v1.xlsx'
        url = urljoin('https://mytoms.ets.org/mt/resources/xls/', file_name)
        self.driver.get(url)
        if self.driver.find_element_by_xpath('//*[text()="HTTP Status 404"]'):
            return '' #TODO: - Fail and let me know.
        return BrowserWait(driver=self.driver).until_file_downloaded()
import json
import re

from selenium.common.exceptions import *

from .caasppbasecontroller import CAASPPBaseController
from webcontrollers.common.errors import *
from wait import BrowserWait
from urllib.parse import urlsplit, urljoin


class TOMSController(CAASPPBaseController):

    def login(self, username: str, password: str, retrieve_login_code=None, **kwargs):
        """
        Logs into TOMS.
        :param username:
        :param password:
        :param retrieve_login_code: A function that returns the login code TOMS emails you.
        """
        self._login(link='https://mytoms.ets.org', username=username, password=password, retrieve_login_code=retrieve_login_code, **kwargs)
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
        try:
            if self.driver.find_element_by_xpath('//*[text()="HTTP Status 404"]'):
                raise FileNotFoundError("This template is no longer available.")
        except NoSuchElementException:
            pass
        return BrowserWait(driver=self.driver).until_file_downloaded()

    def upload_test_settings(self, path: str):
        """Uploads the TOMS Test Settings file."""
        self.driver.get('https://mytoms.ets.org/mt/dt/uploadaccoms.htm')
        self.driver.execute_script("javascript:doStepMove(1);")
        self.driver.find_element_by_xpath("//*[@id='uploadfilepath']").send_keys(path)
        self.driver.execute_script("javascript:doStepMove(1);")

        try:
            if self.driver.find_element_by_xpath('//*[text()="Last file validate attempt was NOT successful. Only .xlsx format files can be uploaded. Please update the file and try uploading again."]'):
                raise InterruptedError("Invalid upload file for TOMS Test Settings.")
        except NoSuchElementException:
            pass

    def test_settings_upload_is_valid(self) -> str:
        """Returns true if the upload was valid, else, returns the file path for the error file."""
        return BrowserWait(timeout=900, poll_frequency=5).until(self._test_settings_upload_is_valid)

    def _test_settings_upload_is_valid(self):
        """Gathers all td elements and uses the 3rd and 4th to validate the last uploaded file."""
        elements = self.driver.find_elements_by_tag_name('td')
        status = elements[3]
        action = elements[4]

        if status.text.startswith('Validated'):
            action.click()
            return True
        elif status.text.startswith('Errors'):
            action.click()
            return BrowserWait(driver=self.driver).until_file_downloaded()
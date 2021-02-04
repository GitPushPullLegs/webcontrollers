from collections import deque
from urllib.parse import urlsplit, urljoin

import requests
from lxml import etree


class CALPADSController:
    _HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    _HOST = 'https://www.calpads.org/'

    def login(self, username: str, password: str):
        """Logs into CALPADS"""
        self.credentials = {
            'Username': username,
            'Password': password
        }
        self.visit_history = deque(maxlen=10)
        self.session = requests.session()
        self.session.headers.update(self._HEADERS)
        self.session.hooks['response'].append(self._event_hooks)

        try:
            self.connection_status = self._login()
        except RecursionError as error:
            print(error)

    def _login(self):
        self.session.get(self._HOST)
        return self.visit_history[-1].status_code == 200 and self.visit_history[-1].url == self._HOST

    def _event_hooks(self, r, *args, **kwargs):
        """Hooks into the request to pull the authorization credentials."""
        scheme, netloc, path, query, frag = urlsplit(r.url)
        print(r.url)
        if path == '/Account/Login' and r.status_code == 200:
            self.session.cookies.update(r.cookies.get_dict())
            init_root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            self.credentials['__RequestVerificationToken'] = \
                init_root.xpath("//input[@name='__RequestVerificationToken']")[0].get('value')
            self.credentials['ReturnUrl'] = init_root.xpath("//input[@id='ReturnUrl']")[0].get('value')
            self.credentials['AgreementConfirmed'] = 'True'
            self.session.post(r.url, data=self.credentials)
        elif path in ['/connect/authorize/callback', '/connect/authorize'] and r.status_code == 200:
            self.session.cookies.update(r.cookies.get_dict())
            login_root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            openid_form_data = {input_.attrib.get('name'): input_.attrib.get('value') for input_ in
                                login_root.xpath('//input')}
            action_url = login_root.xpath('//form')[0].attrib.get('action')
            scheme, netloc, path, query, frag = urlsplit(action_url)
            if not scheme and not netloc:
                self.session.post(urljoin(self._HOST, action_url), data=openid_form_data)
            else:
                self.session.post(action_url, data=openid_form_data)
        else:
            self.visit_history.append(r)
            return r

    def get_leas(self):
        """
        Returns a list of the LEAs.
        """
        response = self.session.get(urljoin(self._HOST, 'LEAS?format=JSON'))
        return response

    def get_schools(self, lea_code: str):
        """
        Returns a list of all the schools in an LEA as JSON.
        :param lea_code: The LEA Code, you can get this from the get_leas def.
        :return: JSON data detailing the schools within the LEA.
        """
        response = self.session.get(urljoin(self._HOST, f"/SchoolListingAll?lea={lea_code}&format=JSON"))
        return response

    def get_enrollment_history(self, ssid):
        """
        Returns a students enrollment history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Enrollment?format=JSON'))
        return response

    def get_demographics(self, ssid):
        """
        Returns a students demographic history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Demographics?format=JSON'))
        return response

    def get_address_history(self, ssid):
        """
        Returns a students address history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Address?format=JSON'))
        return response

    def get_ela(self, ssid):
        """
        Returns a students English Language Acquisition history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/EnglishLanguageAcquisition?format=JSON'))
        return response

    def get_program_history(self, ssid):
        """
        Returns a students program history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Program?format=JSON'))
        return response

    def get_student_course_section_history(self, ssid):
        """
        Returns a students course selection history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/StudentCourseSection?format=JSON'))
        return response

    def get_career_technical_education(self, ssid):
        """
        Returns a students career technical education history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/CareerTechnicalEducation?format=JSON'))
        return response

    def get_student_absence_summary(self, ssid):
        """
        Returns a students absence history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/StudentAbsenceSummary?format=JSON'))
        return response

    def get_incident_result(self, ssid):
        """
        Returns a students incident history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/StudentIncidentResult?format=JSON'))
        return response

    def get_student_offense(self, ssid):
        """
        Returns a students offense history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Offense?format=JSON'))
        return response

    def get_assessment_history(self, ssid):
        """
        Returns a students assessment history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/Assessment?format=JSON'))
        return response

    def get_sped_history(self, ssid):
        """
        Returns a students special education meeting history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/SPED?format=JSON'))
        return response

    def get_sped_service_history(self, ssid):
        """
        Returns a students special education services provided history.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/SSRV?format=JSON'))
        return response

    def get_postsecondary_status(self, ssid):
        """
        Returns a students postsecondary status.
        :param ssid: The students SSID number.
        :return: JSON
        """
        response = self.session.get(urljoin(self._HOST, f'/Student/{ssid}/PSTS?format=JSON'))
        return response

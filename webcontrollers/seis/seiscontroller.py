from webcontrollers.common import WebController
from selenium.common.exceptions import *
from webcontrollers.common.errors import *


class SEISController(WebController):

    def login(self, username: str, password: str):
        print("username")
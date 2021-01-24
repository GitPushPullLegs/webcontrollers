from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webcontrollers.common import WebController
from webcontrollers.common.errors import *


class SchoologyController(WebController):

    def login(self, username:str, password: str):
        print("Hello moto.")
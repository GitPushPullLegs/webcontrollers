from webcontrollers.common import WebController
from selenium.common.exceptions import *
from webcontrollers.common.errors import *


class CERSController(WebController):
    def __init__(self):
        print("Initial class")
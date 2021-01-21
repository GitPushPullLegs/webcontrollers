from selenium import webdriver
import os


class WebController:

    def __init__(self, driver=None, show_window: bool = True, download_path: str = None):
        """
        Spawns a new browser.
        :param driver: A user may pass an existing driver that's already been setup.
        :param show_window: Default is True.
        :param download_path: If not set, will use the
        default download path. If specified but doesn't exist, will create the directory.
        """
        if driver:
            self.driver = driver
            return

        options = webdriver.ChromeOptions()
        if not show_window:
            options.add_argument("--headless")

        if isinstance(download_path, str):
            absolute_download_path = os.path.abspath(download_path)
            if not os.path.isdir(absolute_download_path):
                try:
                    os.makedirs(absolute_download_path)
                    options.add_experimental_option('prefs', {'download.default_directory': absolute_download_path})
                except OSError as os_error:
                    print(f"Unable to create download path. Error: {os_error}")
            else:
                options.add_experimental_option('prefs', {'download.default_directory': absolute_download_path})

        driver_path = os.path.join(os.path.split(__file__)[0], f'drivers{os.path.sep}chromedriver.exe')
        # TODO: Add support for alternate operating systems.

        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

        welcome_path = os.path.join(os.path.split(__file__)[0], f'html{os.path.sep}welcome.html')
        self.driver.get(welcome_path)

    def quit(self):
        self.driver.quit()

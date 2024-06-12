from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverHelper:
    """
    Helper class for initializing and managing WebDriver instances.
    """

    def __init__(self, headless=True):
        """
        Initialize the WebDriverHelper.

        Args:
            headless (bool): Whether to run the browser in headless mode. Defaults to True.
        """
        self.headless = headless
        self.driver = None

    def get_driver_options(self):
        """
        Get the WebDriver options.

        Returns:
            Options: The configured WebDriver options.
        """
        options = Options()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-images")
            options.add_argument("--remote-debugging-port=9229")
        return options

    def initialize_driver(self):
        """
        Initialize the WebDriver.

        Returns:
            WebDriver: The initialized WebDriver instance.
        """
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        return self.driver

    def quit_driver(self):
        """
        Quit the WebDriver instance if it is running.

        Args:
            driver (WebDriver): The WebDriver instance to quit.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None

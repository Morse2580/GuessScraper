import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


class GenericScraperHelper:
    """
    Helper class containing generic methods for web scraping.
    """

    @staticmethod
    def get_soup(driver):
        """
        Retrieve the BeautifulSoup object of the current page.

        Args:
            driver (WebDriver): The WebDriver instance.

        Returns:
            BeautifulSoup: The BeautifulSoup object of the page source.
        """
        return BeautifulSoup(driver.page_source, "html.parser")

    @staticmethod
    def set_driver_for_page_url(driver, relative_category_url, wait_time=10):
        """
        Load a page and wait until the body element is present.

        Args:
            driver (WebDriver): The WebDriver instance.
            relative_category_url (str): The relative URL to load.
            wait_time (int): The time to wait for the body element to load. Defaults to 10 seconds.
        """
        driver.get(relative_category_url)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    @staticmethod
    def load_all_products(driver):
        """
        Scroll down the page to load all products.

        Args:
            driver (WebDriver): The WebDriver instance.
        """
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

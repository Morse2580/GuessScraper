from src.helpers.generic_scraper_helper import GenericScraperHelper
from src.helpers.guess_url_helper import URLConstructorHelper
from src.helpers.web_driver_helper import WebDriverHelper


class GuessScraper:
    """
    Scraper class for extracting product information from the Guess website.
    """

    def __init__(self, BASE_URL, clothing_gender_type, headless=True):
        """
        Initialize the GuessScraper.

        Args:
            BASE_URL (str): The base URL of the website.
            clothing_gender_type (str): The gender type for the clothing (e.g., 'dames', 'heren').
            headless (bool): Whether to run the browser in headless mode. Defaults to True.
        """
        self.BASE_URL = BASE_URL
        self.clothing_gender_type = clothing_gender_type
        self.driver_helper = WebDriverHelper(headless)
        self.driver = self.driver_helper.initialize_driver()
        self.CATEGORY_DROPDOWN_CSS_LIST = (
            "div.mb-lg-0.filters-container__item.refinements__item--category "
            "div.js-collapse.refinements__wrapper.collapse.show div.filters-content "
            "ul.refinements__attribute-wrapper.values.content.pl-0.m-lg-0 "
            "li.refinements__attribute"
        )
        self.all_clothing_items = []

    @staticmethod
    def construct_group_category_url(url, target_group, clothing_url):
        """
        Construct the URL for a group category.

        Args:
            url (str): The base URL.
            target_group (str): The target group (e.g., 'dames', 'heren').
            clothing_url (str): The specific clothing URL parameters.

        Returns:
            str: The constructed URL for the group category.
        """
        return f"{url}/{target_group}/kleding/{clothing_url}"

    @staticmethod
    def construct_clothing_type_category_url(group_category_url, clothing_type):
        """
        Construct the URL for a specific clothing type category.

        Args:
            group_category_url (str): The URL for the group category.
            clothing_type (str): The clothing type to be added to the URL.

        Returns:
            str: The constructed URL for the clothing type category.
        """
        modified_url = re.sub(r"(kleding)", f"\\1/{clothing_type}", group_category_url)
        return modified_url

    @staticmethod
    def construct_url_based_on_params(url, params):
        """
        Construct a URL with additional query parameters.

        Args:
            url (str): The base URL.
            params (dict): Dictionary of query parameters to be added.

        Returns:
            str: The constructed URL with query parameters.
        """
        url_parts = list(urlparse(url))
        query = parse_qs(url_parts[4])
        query.update(params)
        url_parts[4] = urlencode(query, doseq=True)
        return urlunparse(url_parts)

    def click_specific_button(self, button_text):
        """
        Click a specific button on the page.

        Args:
            button_text (str): The text of the button to click.

        Raises:
            Exception: If the button cannot be clicked after several attempts.
        """
        attempts = 3
        for attempt in range(attempts):
            try:
                button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f"//div[contains(@class, 'refinements__item-button') and .//span[text()='{button_text}']]",
                        )
                    )
                )
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                clickable_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//div[contains(@class, 'refinements__item-button') and .//span[text()='{button_text}']]",
                        )
                    )
                )
                self.driver.execute_script("arguments[0].click();", clickable_button)
                return
            except WebDriverException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)
        raise Exception("Failed to click the dropdown button after several attempts")

    def extract_clothing_type_titles(self, css_dropdown_list):
        """
        Extract clothing type titles from the dropdown list.

        Args:
            css_dropdown_list (str): The CSS selector for the dropdown list.

        Returns:
            list: A list of extracted clothing type titles.
        """
        titles = []
        try:
            list_items = self.driver.find_elements(By.CSS_SELECTOR, css_dropdown_list)
            for item in list_items:
                title = item.get_attribute("title")
                if title:
                    title = self.convert_to_dash_format(title)
                    titles.append(title)
        except Exception as e:
            print(f"Exception occurred while extracting titles: {e}")
        return titles

    def extract_product_info(self, str_gender):
        """
        Extract product information from the current page.

        Args:
            str_gender (str): The gender type for the clothing (e.g., 'dames', 'heren').

        Returns:
            list: A list of dictionaries containing product information.
        """
        soup = GenericScraperHelper.get_soup(self.driver)
        products = []
        try:
            description_divs = soup.select("div.small-description")
            for grid in description_divs:
                product_divs = grid.select("div.pdp-link.product-tile__pdp-link")
                for div in product_divs:
                    title = self.extract_title_info(div)
                    price_container = div.find_next("div", class_="product__price")

                    if price_container:
                        original_price, sale_price = self.extract_price_info(
                            price_container
                        )

                        product_info = {
                            "title": title,
                            "original_price": original_price,
                            "sale_price": sale_price,
                            "gender": str_gender,
                        }
                        products.append(product_info)
        except Exception as e:
            print(f"Exception occurred while extracting product information: {e}")
        return products

    @staticmethod
    def extract_price_info(price_container):
        """
        Extract price information from the price container.

        Args:
            price_container (Tag): The BeautifulSoup tag containing price information.

        Returns:
           tuple: A tuple containing original price and sale price.
        """
        original_price_tag = price_container.find(
            "span", class_="price__strike-through"
        )
        if original_price_tag is None:
            original_price_tag = price_container.find(
                "span", class_="value price__value"
            )
        sale_price_tag = price_container.find("span", class_="value price__value--sale")

        original_price = (
            original_price_tag.get_text(strip=True) if original_price_tag else ""
        )
        sale_price = sale_price_tag.get_text(strip=True) if sale_price_tag else ""

        return original_price, sale_price

    @staticmethod
    def extract_title_info(product_div):
        """
        Extract the title information from the product div.

        Args:
            product_div (Tag): The BeautifulSoup tag containing product information.

        Returns:
            str: The extracted title information.
        """
        title_tag = product_div.find("a", class_="link product-tile__link js-tile-link")
        return title_tag.get_text(strip=True) if title_tag else ""

    @staticmethod
    def convert_to_dash_format(title):
        """
        Convert a title to dash-separated format.

        Args:
            title (str): The title to be converted.

        Returns:
            str: The dash-separated title.
        """
        cleaned_phrase = title.lower().strip()
        dash_format = cleaned_phrase.replace(" ", "-").lower()
        return dash_format

    def create_clothing_links_from_titles(self, url, titles):
        """
        Create clothing type URLs from titles.

        Args:
            url (str): The base URL.
            titles (list): A list of clothing type titles.

        Returns:
            list: A list of constructed clothing type URLs.
        """
        clothing_type_urls = []
        for title in titles:
            clothing_type_urls.append(
                self.construct_clothing_type_category_url(url, title)
            )
        return clothing_type_urls

    def scrape(self, clothing_base_urls):
        """
        Scrape product information from the given clothing base URLs.

        Args:
            clothing_base_urls (list): A list of base URLs for different clothing categories.

        Returns:
            list: A list of dictionaries containing product information.
        """
        for clothing_url in clothing_base_urls:
            relative_clothing_category_url = (
                URLConstructorHelper.construct_group_category_url(
                    self.BASE_URL, self.clothing_gender_type, clothing_url
                )
            )
            GenericScraperHelper.set_driver_for_page_url(
                self.driver, relative_clothing_category_url
            )
            self.click_specific_button("Op categorie")
            time.sleep(2)
            titles = self.extract_clothing_type_titles(self.CATEGORY_DROPDOWN_CSS_LIST)
            clothing_type_urls = self.create_clothing_links_from_titles(
                relative_clothing_category_url, titles
            )

            self.driver_helper.quit_driver()
            for clothing_type_url in clothing_type_urls:
                if clothing_type_url is None:
                    break
                self.driver = self.driver_helper.initialize_driver()
                GenericScraperHelper.set_driver_for_page_url(
                    self.driver, clothing_type_url
                )
                GenericScraperHelper.load_all_products(self.driver)
                products = self.extract_product_info(
                    str_gender=self.clothing_gender_type
                )
                self.all_clothing_items.append(products)
                self.driver_helper.quit_driver()

        return self.all_clothing_items

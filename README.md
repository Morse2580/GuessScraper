#### Guess Scraper

##### Overview

The GuessScraper is a Python class designed to scrape product information from the Guess website. It leverages Selenium and BeautifulSoup to navigate through the website, extract relevant data, and handle various web elements. The scraper supports headless browsing, making it efficient for automated environments.

###### Features

	-	Headless Browsing: Runs the browser in headless mode for efficiency.
	-	Dynamic URL Construction: Constructs URLs for different clothing categories and types.
	-	Automated Button Clicks: Handles button clicks dynamically on the webpage.
	-	Data Extraction: Extracts product titles and prices, including original and sale prices.
	-	Scalable and Maintainable: Designed with scalability and maintainability in mind.

###### Prerequisites

	-	Python 3.x
	-	Selenium
	-	BeautifulSoup
	-	WebDriver Manager for Chrome

###### Installation

	1.	Clone the repository:
    ```
        git clone https://github.com/yourusername/guess-scraper.git
        cd guess-scraper
    ```

	2.	Install the required Python packages:  

    ```
        pip install -r requirements.txt
    ```

    ```
    guess-scraper/
        ├── src/
        │   ├── helpers/
        │   │   ├── generic_scraper_helper.py
        │   │   ├── guess_url_helper.py
        │   │   └── web_driver_helper.py
        │   └── guess_scraper.py
        ├── main.py
        ├── requirements.txt
        └── README.md
    ```

###### Usage

###### Initialize the Scraper

To initialize and use the GuessScraper, follow these steps:

	1.	Import the necessary modules:

    ```
        from src.helpers.generic_scraper_helper import GenericScraperHelper
        from src.helpers.guess_url_helper import URLConstructorHelper
        from src.helpers.web_driver_helper import WebDriverHelper
        from src.guess_scraper import GuessScraper
    ```

    2.	Set up base URLs and gender types:

    ```
        BASE_URL = "https://www.guess.eu/nl-be/guess"
        CLOTHING_URL = "?prefn1=guess_visibleInCountries&prefv1=BE%7CALL&psubcat=true"
        SALE_URL = "?prefn1=guess_visibleInCountries&prefv1=BE%7CALL&prefn2=isSale&prefv2=BE"
        CLOTHING_BASE_URLS = [CLOTHING_URL, SALE_URL]
        clothing_gender_types = ["dames", "heren"]
    ```

    3.	Scrape the data:

    ```
        for clothing_gender_type in clothing_gender_types:
        scraper = GuessScraper(BASE_URL=BASE_URL, clothing_gender_type=clothing_gender_type)
        scraped_data = scraper.scrape(CLOTHING_BASE_URLS)
        print(scraped_data)
    ```
###### Classes and Methods

###### WebDriverHelper

A helper class for initializing and managing WebDriver instances.

	•	Methods:
	•	__init__(self, headless=True): Initializes the helper with headless option.
	•	get_driver_options(self): Returns the WebDriver options.
	•	initialize_driver(self): Initializes and returns the WebDriver instance.
	•	quit_driver(self): Quits the WebDriver instance.

###### GenericScraperHelper

A helper class containing generic methods for web scraping.

	•	Methods:
	•	get_soup(driver): Returns the BeautifulSoup object of the current page.
	•	set_driver_for_page_url(driver, relative_category_url, wait_time=10): Loads a page and waits until the body element is present.
	•	load_all_products(driver): Scrolls down the page to load all products.

###### URLConstructorHelper

A helper class for constructing URLs for different clothing categories.

	•	Methods:
	•	construct_group_category_url(base_url, target_group, clothing_url): Constructs the URL for a group category.
	•	construct_clothing_type_category_url(group_category_url, clothing_type): Constructs the URL for a specific clothing type category.
	•	construct_url_based_on_params(base_url, params): Constructs a URL with additional query parameters.

###### GuessScraper

The main scraper class for extracting product information from the Guess website.

	•	Methods:
	•	__init__(self, BASE_URL, clothing_gender_type, headless=True): Initializes the scraper.
	•	click_specific_button(self, button_text): Clicks a specific button on the page.
	•	extract_clothing_type_titles(self, css_dropdown_list): Extracts clothing type titles from the dropdown list.
	•	extract_product_info(self, str_gender): Extracts product information from the current page.
	•	extract_price_info(price_container): Extracts price information from the price container.
	•	extract_title_info(product_div): Extracts the title information from the product div.
	•	convert_to_dash_format(title): Converts a title to dash-separated format.
	•	create_clothing_links_from_titles(self, url, titles): Creates clothing type URLs from titles.
	•	scrape(self, clothing_base_urls): Scrapes product information from the given clothing base URLs.

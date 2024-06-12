import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class URLConstructorHelper:
    """
    Helper class for constructing URLs for different clothing categories.
    """

    @staticmethod
    def construct_group_category_url(base_url, target_group, clothing_url):
        """
        Construct the URL for a group category.

        Args:
            base_url (str): The base URL of the website.
            target_group (str): The target group (e.g., 'dames', 'heren').
            clothing_url (str): The specific clothing URL parameters.

        Returns:
            str: The constructed URL for the group category.
        """
        return f"{base_url}/{target_group}/kleding/{clothing_url}"

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
    def construct_url_based_on_params(base_url, params):
        """
        Construct a URL with additional query parameters.

        Args:
            base_url (str): The base URL.
            params (dict): Dictionary of query parameters to be added.

        Returns:
            str: The constructed URL with query parameters.
        """
        url_parts = list(urlparse(base_url))
        query = parse_qs(url_parts[4])
        query.update(params)
        url_parts[4] = urlencode(query, doseq=True)
        return urlunparse(url_parts)

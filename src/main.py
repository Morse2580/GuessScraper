from scraper.guess_scaper import GuessScraper
if __name__ == "__main__":
    BASE_URL = "https://www.guess.eu/nl-be/guess"
    CLOTHING_URL = "?prefn1=guess_visibleInCountries&prefv1=BE%7CALL&psubcat=true"
    SALE_URL = "?prefn1=guess_visibleInCountries&prefv1=BE%7CALL&prefn2=isSale&prefv2=BE"
    CLOTHING_BASE_URLS = [CLOTHING_URL, SALE_URL]
    clothing_gender_types = ["dames", "heren"]

    for clothing_gender_type in clothing_gender_types:
        scraper = GuessScraper(base_url=BASE_URL, clothing_gender_type=clothing_gender_type)
        scraped_data = scraper.scrape(CLOTHING_BASE_URLS)
        print(scraped_data)
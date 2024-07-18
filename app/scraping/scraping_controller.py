import logging
from bs4 import BeautifulSoup
from app.scraping.http_client import HttpClient
from app.scraping.website.register import WebsiteScapingRegister

class ScrapingController:

    def __init__(self, http_client, bs4_factory, website_scraping_register):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.logger.info("Initialization Started")
        self.http_client: HttpClient = http_client
        self.bs4_factory: BeautifulSoup = bs4_factory
        self.website_scraping_register: WebsiteScapingRegister = website_scraping_register

    def initialize_resources(self, scraping_template_service):
        self.website_scraping_register.register_enabled_websites(scraping_template_service)
        self.logger.info("Initialization Completed")

    async def get_scraped_data(self, url):
        html_content = await self.http_client.get(url)
        soup = self.bs4_factory(html_content, 'html.parser')
        return soup
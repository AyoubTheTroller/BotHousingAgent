from dependency_injector import containers, providers
from bs4 import BeautifulSoup
from app.scraping.http_client import HttpClient
from app.scraping.scraping_controller import ScrapingController
from app.scraping.website.register import WebsiteScapingRegister


class ScrapingContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    http_client = providers.Singleton(HttpClient)

    bs4_factory = providers.Factory(BeautifulSoup)

    website_scraping_register = providers.Singleton(
        WebsiteScapingRegister
    )

    scraping_controller = providers.Singleton(
        ScrapingController,
        http_client=http_client,
        bs4_factory=bs4_factory,
        website_scraping_register=website_scraping_register
    )

from dependency_injector import containers, providers
from bs4 import BeautifulSoup
from app.scraping.http_client import HttpClient
from app.scraping.scraping_controller import ScrapingController
from app.scraping.website.register import WebsiteScapingRegister


class ScrapingContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    http_client_factory = providers.Factory(HttpClient)

    bs4_factory = providers.Factory(BeautifulSoup)

    website_scraping_register = providers.Singleton(
        WebsiteScapingRegister
    )

    scraping_controller = providers.Singleton(
        ScrapingController,
        http_client_factory=http_client_factory.provider,
        bs4_factory=bs4_factory.provider,
        website_scraping_register=website_scraping_register
    )

import logging
from typing import Dict
from app.scraping.website.base_loader import BaseLoader
from app.scraping.website.url.builder import UrlBuilder
from app.service.template.scraping.template_service import ScrapingTemplateService

class WebsiteScapingRegister:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.website_url_builders: Dict[str, UrlBuilder] = {}
    
    def register_enabled_websites(self, template_service: ScrapingTemplateService):
        enabled_websites = template_service.get_managed_websites()
        for website in enabled_websites:
            self.register_url_builder(website, BaseLoader(template_service, website, "url"))
        self.logger.info("Enabled Websites Registered")

    def register_url_builder(self, website_name: str, loader: BaseLoader):
        self.website_url_builders[website_name] = UrlBuilder(loader)

    def get_url_builder(self, website_name: str) -> UrlBuilder:
        builder = self.website_url_builders.get(website_name)
        if not builder:
            raise ValueError(f"No builder registered for website: {website_name}")
        return builder

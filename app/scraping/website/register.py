import logging
from typing import Dict
from app.scraping.website.base_loader import BaseLoader
from app.scraping.website.url.builder import UrlBuilder
from app.scraping.website.search_result.parser import SearchResultParser
from app.service.template.scraping.template_service import ScrapingTemplateService

class WebsiteScapingRegister:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self._website_url_builders: Dict[str, UrlBuilder] = {}
        self._website_search_result_parsers: Dict[str, SearchResultParser] = {}
    
    def register_enabled_websites(self, template_service: ScrapingTemplateService):
        enabled_websites = template_service.get_managed_websites()
        for website in enabled_websites:
            self.register_url_builder(website, BaseLoader(template_service, website, "url"))
            self.register_search_result_parsers(website, BaseLoader(template_service, website, "search_result"))
        self.logger.info("Enabled Websites Registered")

    def register_url_builder(self, website_name: str, loader: BaseLoader):
        self._website_url_builders[website_name] = UrlBuilder(loader)

    def register_search_result_parsers(self, website_name: str, loader: BaseLoader):
        self._website_search_result_parsers[website_name] = SearchResultParser(loader)

    def get_url_builder(self, website_name: str) -> UrlBuilder:
        builder = self._website_url_builders.get(website_name)
        if not builder:
            raise ValueError(f"No builder registered for website: {website_name}")
        return builder

    def get_search_result_parser(self, website_name: str) -> SearchResultParser:
        search_result_parser = self._website_search_result_parsers.get(website_name)
        if not search_result_parser:
            raise ValueError(f"No search result parses registered for website: {website_name}")
        return search_result_parser

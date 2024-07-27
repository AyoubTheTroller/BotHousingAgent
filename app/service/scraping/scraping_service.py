from app.scraping.scraping_controller import ScrapingController
from app.service.template.scraping.template_service import ScrapingTemplateService

class ScrapingService:
    def __init__(self,
                 scraping_controller: ScrapingController,
                 scraping_template_service: ScrapingTemplateService):
        
        self.scraping_controller = scraping_controller
        self.scraping_template_service = scraping_template_service
        self.initialize_scraping_resources()

    def initialize_scraping_resources(self):
        self.scraping_controller.initialize_resources(self.scraping_template_service)

    async def build_url(self, query_params):
        url_builder = self.scraping_controller.website_scraping_register.get_url_builder("immobiliare")
        return url_builder.build_url(query_params)

    async def scrape_listings(self, url):
        soup = await self.scraping_controller.get_scraped_data(url)
        search_result_parser = self.scraping_controller.website_scraping_register.get_search_result_parser("immobiliare")
        data = await search_result_parser.extract_json_from_script(soup)
        return await search_result_parser.get_house_listings(data)
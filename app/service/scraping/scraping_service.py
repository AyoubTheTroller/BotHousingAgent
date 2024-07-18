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
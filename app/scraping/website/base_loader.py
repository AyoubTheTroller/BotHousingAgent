from app.service.template.scraping.template_service import ScrapingTemplateService

class BaseLoader():
    def __init__(self,
                 template_service: ScrapingTemplateService,
                 website: str,
                 resource: str):

        self.template_service = template_service
        self.website = website
        self.resource = resource

    def get_template(self, *keys, **kwargs):
        """Helper function to return the message from a template."""
        return self.template_service.render_template(self.website, self.resource, *keys, **kwargs)

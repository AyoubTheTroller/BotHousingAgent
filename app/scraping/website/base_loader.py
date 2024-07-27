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
    
    def load_json_parsing_keys(self) -> dict:
        json_object: dict = self.get_template("json_object")
        parsing_keys: dict = {}
        for key, value in json_object.items():
            parsing_keys[key] = self.split_keys(value)
        return parsing_keys

    def split_keys(self, path: str) -> list:
        """Splits a dot-separated string into a list of keys."""
        return path.split('.')

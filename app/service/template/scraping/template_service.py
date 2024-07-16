from pystache import Renderer
from app.template.scraping.scraping_templates import ScrapingTemplates

class ScrapingTemplateService:

    def __init__(self, scraping_templates):
        self._scraping_templates: ScrapingTemplates = scraping_templates
    
    def render_template(self, template_type, template_name: str, *keys, **kwargs) -> str:
        """Renders a Telegram template."""
        template = self._scraping_templates.get_template(template_type, template_name, keys)
        if isinstance(template, str):
            return self.render(template, **kwargs)
        return template

    def render(self, template, **kwargs) -> str:
        renderer = Renderer()
        return renderer.render(template, kwargs)

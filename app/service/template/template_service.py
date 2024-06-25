from pystache import Renderer

class TemplateService:

    def __init__(self, telegram_templates):
        self._telegram_templates = telegram_templates

    def render_telegram_template(self, template_type, template_name: str, key: str, **kwargs) -> str:
        """Renders a Telegram template."""
        template = self._telegram_templates.get_template(template_type, template_name)
        to_be_rendered = template.get(key)
        return self.render_template(to_be_rendered, **kwargs)

    def render_template(self, template, **kwargs) -> str:
        renderer = Renderer()
        return renderer.render(template, kwargs)

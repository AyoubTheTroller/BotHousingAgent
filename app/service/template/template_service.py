from pystache import Renderer

class TemplateService:

    def __init__(self, telegram_templates):
        self._telegram_templates = telegram_templates

    def render_telegram_template(self, template_type, template_name: str, category: str, key: str, **kwargs) -> str:
        """Renders a Telegram template."""
        template = self._telegram_templates.get_template(template_type, template_name, category)
        value = template.get(key)
        if isinstance(value, str):
            return self.render_template(value, **kwargs)
        return value

    def render_template(self, template, **kwargs) -> str:
        renderer = Renderer()
        return renderer.render(template, kwargs)

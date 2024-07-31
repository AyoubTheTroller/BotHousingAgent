from pystache import Renderer
from app.template.telegram.telegram_templates import TelegramTemplates

class TelegramTemplateService:

    def __init__(self, telegram_templates):
        self._telegram_templates: TelegramTemplates = telegram_templates
    
    async def render_template(self,language, template_type, template_name: str, *keys, **kwargs) -> str:
        """Renders a Telegram template."""
        template = await self._telegram_templates.get_template(language, template_type, template_name, *keys)
        if isinstance(template, str):
            return self.render(template, **kwargs)
        return template

    def render(self, template, **kwargs) -> str:
        renderer = Renderer()
        return renderer.render(template, kwargs)

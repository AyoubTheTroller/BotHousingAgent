
class TemplateRenderer:
    def __init__(self, template_data: dict):
        self._templates = template_data

    def render_template(self, language: str, template_name: str, **kwargs):
        """Renders a template for a specific language with the given context."""
        language_templates = self._templates.get(language, {})
        template_str = language_templates.get(template_name, "")
        return template_str.format(**kwargs)
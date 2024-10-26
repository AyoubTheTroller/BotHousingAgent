from app.utils.data_loader import DataLoader

class TelegramTemplates:
    """Loads and manages Telegram bot templates."""

    def __init__(self, templates_path, language):
        self._templates_path = templates_path+"telegram/"
        self._language = language
        self._templates = self._load_templates()

    def _load_templates(self) -> dict:
        """Loads templates based on the configuration."""
        templates = {}
        # Load the managed templates configuration
        managed_templates = DataLoader.load_json(self._templates_path+"managed.json")
        for key, value in managed_templates.items():
            templates[key] = {}
            for active_template in value.get("active"):
                template = DataLoader.load_json(self._templates_path+key+"/"+active_template+"/"+"template.json")
                templates[key][active_template]=template
        return templates
    
    async def get_template_with_language(self, language, template_type, template_category, *keys) -> str:
        """
        Extracts the correct template from a given template dictionary using type, category, and nested keys.
        """
        template = self._templates.get(template_type, {}).get(template_category, {})
        for key in keys:
            template = template.get(key, {})
        # Filter the final dictionary based on the language
        if language is None:
            language = self._language
        return template.get(language, {})
    
    def get_template(self, template_type, template_category, *keys) -> str:
        """
        Extracts the correct template from a given template dictionary using type, category, and nested keys.
        """
        template = self._templates.get(template_type, {}).get(template_category, {})
        for key in keys:
            template = template.get(key, {})
        return template
    
    @property
    def templates(self):
        return self._templates

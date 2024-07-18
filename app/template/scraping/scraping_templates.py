from app.utils.data_loader import DataLoader

class ScrapingTemplates:
    """Loads and manages Telegram bot templates."""

    def __init__(self, templates_path):
        self._templates_path = templates_path+"scraping/"
        self._templates, self._managed_websites = self._load_templates()

    def _load_templates(self) -> dict:
        """Loads templates based on the configuration."""
        templates = {}
        managed_websites = []
        # Load the managed templates configuration
        managed_templates = DataLoader.load_json(self._templates_path+"managed.json")
        for key, value in managed_templates.items():
            templates[key] = {}
            managed_websites.append(key)
            for active_template in value.get("active"):
                template = DataLoader.load_json(self._templates_path+key+"/"+active_template+"/"+"template.json")
                templates[key][active_template]=template
        return templates, managed_websites

    def get_template(self, template_type, template_category, *keys) -> str:
        """
        Extracts the correct template from a given template dictionary using type, category, and nested keys.
        """
        template = self._templates.get(template_type, {}).get(template_category, {})
        for key in keys:
            template = template.get(key, {})
        return template

    def get_managed_websites(self):
        """Extracts the list of managed websites"""
        return self._managed_websites

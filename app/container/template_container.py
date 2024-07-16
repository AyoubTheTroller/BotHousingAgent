from dependency_injector import containers, providers
from app.template.telegram.telegram_templates import TelegramTemplates
from app.template.scraping.scraping_templates import ScrapingTemplates

class TemplateContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    telegram_templates = providers.Singleton(
        TelegramTemplates,
        templates_path=config.paths.templates,
        language=config.language.templates
    )

    scraping_templates = providers.Singleton(
        ScrapingTemplates,
        templates_path=config.paths.templates
    )

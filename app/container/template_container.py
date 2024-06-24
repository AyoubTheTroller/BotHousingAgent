from dependency_injector import containers, providers
from app.template.telegram.telegram_templates import TelegramTemplates

class TemplateContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    telegram_templates = providers.Singleton(
        TelegramTemplates,
        templates_path=config.paths.templates,
        language=config.language.templates
    )

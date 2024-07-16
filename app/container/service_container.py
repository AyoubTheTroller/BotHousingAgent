from dependency_injector import containers, providers
from app.service.mongodb.mongo_service import MongoService
from app.service.template.telegram.template_service import TelegramTemplateService
from app.service.template.scraping.template_service import ScrapingTemplateService

class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_client = providers.Dependency()

    templates = providers.DependenciesContainer()

    mongo_service = providers.Factory(
        MongoService,
        mongo_client,
    )

    telegram_template_service = providers.Factory(
        TelegramTemplateService,
        telegram_templates=templates.telegram_templates
    )

    scraping_template_service = providers.Factory(
        ScrapingTemplateService,
        scraping_templates=templates.scraping_templates
    )

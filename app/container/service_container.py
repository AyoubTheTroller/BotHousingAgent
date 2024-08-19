from dependency_injector import containers, providers
from app.service.mongodb.mongo_service import MongoService
from app.service.template.telegram.template_service import TelegramTemplateService
from app.service.template.scraping.template_service import ScrapingTemplateService
from app.service.scraping.scraping_service import ScrapingService
from app.service.search.search_service import SearchService
from app.service.mongodb.dao_controller_service import DaoControllerService

class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_client = providers.Dependency()

    templates = providers.DependenciesContainer()

    scraping = providers.DependenciesContainer()

    mongo_service = providers.Factory(
        MongoService,
        mongo_client,
    )

    dao_controller_service = providers.Singleton(
        DaoControllerService,
        mongo_client
    )

    telegram_template_service = providers.Factory(
        TelegramTemplateService,
        telegram_templates=templates.telegram_templates
    )

    scraping_template_service = providers.Factory(
        ScrapingTemplateService,
        scraping_templates=templates.scraping_templates
    )

    scraping_service = providers.Singleton(
        ScrapingService,
        scraping_controller=scraping.scraping_controller,
        scraping_template_service=scraping_template_service
    )

    search_service_factory = providers.Factory(
        SearchService,
        scraping_service=scraping_service
    )

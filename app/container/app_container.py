from dependency_injector import containers, providers
from app.container.core_container import CoreContainer
from app.container.db_container import DbContainer
from app.container.telegram_container import TelegramContainer
from app.container.service_container import ServiceContainer
from app.container.template_container import TemplateContainer
from app.container.scraping_container import ScrapingContainer
from app.config.config_loader import ConfigLoader

class ApplicationContainer(containers.DeclarativeContainer):

    config_loader = ConfigLoader("global-env.json")

    global_config = config_loader.load_global_config_provider()

    app_config = config_loader.load_app_config_provider()

    core = providers.Container(
        CoreContainer,
        config=app_config.core
    )

    templates = providers.Container(
        TemplateContainer,
        config=global_config
    )

    mongodb = providers.Container(
        DbContainer,
        config=app_config,
    )

    scraping = providers.Container(
        ScrapingContainer,
        config=app_config,
    )

    services = providers.Container(
        ServiceContainer,
        config=app_config,
        mongo_client=mongodb.mongo_client,
        templates=templates,
        scraping=scraping
    )

    telegram = providers.Container(
        TelegramContainer,
        config=app_config,
        mongo_service=services.mongo_service,
        template_service=services.telegram_template_service,
        scraping_service = services.scraping_service
    )

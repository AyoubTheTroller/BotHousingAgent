from dependency_injector import containers, providers
from app.container.core_container import CoreContainer
from app.container.db_container import DbContainer
from app.container.telegram_container import TelegramContainer
from app.container.service_container import ServiceContainer
from app.container.template_container import TemplateContainer
from app.container.scraping_container import ScrapingContainer

class ApplicationContainer(containers.DeclarativeContainer):

    core: CoreContainer = providers.Container(
        CoreContainer
    )

    templates = providers.Container(
        TemplateContainer,
        config=core.global_config
    )

    db: DbContainer = providers.Container(
        DbContainer,
        config=core.app_config,
    )

    scraping = providers.Container(
        ScrapingContainer,
        config=core.app_config,
        event_loop=core.event_loop
    )

    services: ServiceContainer = providers.Container(
        ServiceContainer,
        config=core.app_config,
        mongo_client=db.mongo_client,
        templates=templates,
        scraping=scraping
    )

    telegram: TelegramContainer = providers.Container(
        TelegramContainer,
        config=core.app_config,
        services=services,
        event_loop=core.event_loop
    )

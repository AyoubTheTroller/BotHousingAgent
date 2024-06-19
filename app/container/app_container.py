from dependency_injector import containers, providers
from app.container.core_container import CoreContainer
from app.container.db_container import DbContainer
from app.container.telegram_container import TelegramContainer
from app.container.service_container import ServiceContainer
from app.config.config_loader import ConfigLoader

class ApplicationContainer(containers.DeclarativeContainer):

    config = ConfigLoader("global-env.json").load_config_provider()
    
    core = providers.Container(
        CoreContainer,
        config=config.core
    )

    mongodb_package = providers.Container(
        DbContainer,
        config=config,
    )

    services = providers.Container(
        ServiceContainer,
        config=config,
        mongo_client=mongodb_package.mongo_client,
    )

    tg_package = providers.Container(
        TelegramContainer,
        config=config,
        mongo_service=services.mongo_service
    )

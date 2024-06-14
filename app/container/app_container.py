from dependency_injector import containers, providers
from app.container.core_container import CoreContainer
from app.container.db_container import DbContainer
from app.container.telegram_container import TelegramContainer

class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration("config")

    core = providers.Container(
        CoreContainer,
        config=config.core
    )

    mongodb = providers.Container(
        DbContainer,
        config=config,
    )

    tg_app = providers.Container(
        TelegramContainer,
        config=config,
    )

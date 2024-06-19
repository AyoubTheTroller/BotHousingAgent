from dependency_injector import containers, providers
from app.service.mongodb.mongo_service import MongoService
from app.service.telegram.telegram_service import TelegramService

class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_client = providers.Dependency()

    tg_app = providers.Dependency()

    mongo_service = providers.Factory(
        MongoService,
        mongo_client,
    )

    telegram_service = providers.Factory(
        TelegramService,
    )

from dependency_injector import containers, providers
from app.telegram.tg_app import TelegramApplication
from app.telegram.tg_app_builder import TelegramApplicationBuilder
from app.telegram.command_handlers import CommandHandlers

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_service = providers.Dependency()

    telegram_application_builder = providers.Singleton(
        TelegramApplicationBuilder,
        token=config.telegram.token,
    )

    command_handlers = providers.Singleton(CommandHandlers, mongo_service=mongo_service)

    telegram_application = providers.Factory(
        TelegramApplication,
        command_handlers=command_handlers
    )

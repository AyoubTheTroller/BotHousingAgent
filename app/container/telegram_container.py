from dependency_injector import containers, providers
from app.telegram.tg_app import TelegramApplication
from app.telegram.tg_app_builder import TelegramApplicationBuilder
from app.telegram.conversation_handlers import ConversationHandlers

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_service = providers.Dependency()

    template_service = providers.Dependency()

    telegram_application_builder = providers.Singleton(
        TelegramApplicationBuilder,
        token=config.telegram.token,
    )

    conversation_handlers = providers.Singleton(
        ConversationHandlers,
        mongo_service=mongo_service,
        template_service=template_service
    )

    telegram_application = providers.Singleton(
        TelegramApplication,
        command_handlers=conversation_handlers
    )

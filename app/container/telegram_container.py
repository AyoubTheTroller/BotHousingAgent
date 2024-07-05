from dependency_injector import containers, providers
from aiogram import Router, Dispatcher
from app.telegram.tg_app import TelegramApplication
from app.telegram.bot_builder import BotBuilder
from app.telegram.bot_dispatcher import BotDispatcher

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_service = providers.Dependency()

    template_service = providers.Dependency()

    bot_builder = providers.Singleton(
        BotBuilder,
        token=config.telegram.token,
    )

    router_dispatcher = providers.Singleton(
        Dispatcher
    )

    router_factory = providers.Factory(
        Router
    )

    bot_dispatcher = providers.Singleton(
        BotDispatcher,
        mongo_service=mongo_service,
        template_service=template_service,
        dispatcher=router_dispatcher,
        router_factory=router_factory.provider,
    )

    telegram_application = providers.Singleton(
        TelegramApplication,
        bot_dispatcher=bot_dispatcher
    )

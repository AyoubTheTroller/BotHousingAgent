from dependency_injector import containers, providers
from aiogram import Router, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.telegram.tg_app import TelegramApplication
from app.telegram.bot_controller import BotController
from app.telegram.notification.event_emitter import EventEmitter

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_service = providers.Dependency()

    template_service = providers.Dependency()

    bot_default_properties = providers.Singleton(
        DefaultBotProperties,
        parse_mode=ParseMode.HTML
    )

    bot = providers.Singleton(
        Bot,
        token=config.telegram.token,
        default=bot_default_properties
    )

    event_emitter = providers.Singleton(
        EventEmitter
    )

    router_dispatcher = providers.Singleton(
        Dispatcher
    )

    router_factory = providers.Factory(
        Router
    )

    bot_controller = providers.Singleton(
        BotController,
        bot=bot,
        mongo_service=mongo_service,
        template_service=template_service,
        event_emitter=event_emitter,
        dispatcher=router_dispatcher,
        router_factory=router_factory.provider,
    )

    telegram_application = providers.Singleton(
        TelegramApplication,
        bot_controller=bot_controller
    )

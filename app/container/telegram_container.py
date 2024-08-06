from dependency_injector import containers, providers
from aiogram import Router, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.telegram.tg_app import TelegramApplication
from app.telegram.bot_controller import BotController
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.notification.event_emitter import EventEmitter
from app.container.service_container import ServiceContainer

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    services: ServiceContainer = providers.DependenciesContainer()

    event_loop = providers.Dependency()

    bot_default_properties = providers.Singleton(
        DefaultBotProperties,
        parse_mode=ParseMode.HTML
    )

    bot = providers.Singleton(
        Bot,
        token=config.telegram.token,
        default=bot_default_properties
    )

    loader_controller = providers.Singleton(
        LoaderController,
        template_service=services.telegram_template_service
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
        loader_controller=loader_controller,
        mongo_service=services.mongo_service,
        scraping_service=services.scraping_service,
        event_emitter=event_emitter,
        dispatcher=router_dispatcher,
        router_factory=router_factory.provider,
        search_service_factory=services.search_service_factory.provider
    )

    telegram_application = providers.Singleton(
        TelegramApplication,
        bot_controller=bot_controller,
        event_loop=event_loop
    )

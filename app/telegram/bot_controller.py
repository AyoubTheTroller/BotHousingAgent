import logging
from aiogram import Dispatcher, Bot
from dependency_injector import providers
from app.telegram.notification.event_emitter import EventEmitter
from app.telegram.notification.register import EventEmitterRegister
from app.telegram.middleware.register import MiddlewareRegister
from app.telegram.handler.conversation.register import ConversationRegister
from app.telegram.handler.presentation.register import PresentationRegister
from app.telegram.handler.menu.register import MenuRegister
from app.telegram.handler.account.register import AccountRegister
from app.telegram.handler.admin.register import AdminRegister

class BotController:

    def __init__(self,
                 bot:Bot,
                 loader_controller,
                 mongo_service,
                 scraping_service,
                 event_emitter: EventEmitter,
                 dispatcher: Dispatcher,
                 router_factory: providers.Provider,
                 search_service_factory: providers.Provider):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.logger.info("Initialization Started")
        self.bot: Bot = bot
        self.loader_controller = loader_controller
        self.dispatcher = dispatcher
        self.set_dispatcher_dependencies(event_emitter, mongo_service, scraping_service, search_service_factory)
        self.register_event_emitters()
        self.register_middlewares()
        self.register_handlers(router_factory)
        self.logger.info("Initialization Completed")

    def set_dispatcher_dependencies(self, event_emitter, mongo_service, scraping_service, search_service_factory):
        self.dispatcher["event_emitter"] = event_emitter
        self.dispatcher["mongo_service"] = mongo_service
        self.dispatcher["scraping_service"] = scraping_service
        self.dispatcher["search_service_factory"] = search_service_factory

    def register_middlewares(self):
        MiddlewareRegister(self.dispatcher, self.loader_controller)

    def register_event_emitters(self):
        EventEmitterRegister(self.dispatcher, self.bot, self.loader_controller)

    def register_handlers(self, router_factory):
        AdminRegister(self.dispatcher, router_factory, self.loader_controller)
        PresentationRegister(self.dispatcher, router_factory, self.loader_controller)
        ConversationRegister(self.dispatcher, router_factory, self.loader_controller)
        MenuRegister(self.dispatcher, router_factory, self.loader_controller)
        AccountRegister(self.dispatcher, router_factory, self.loader_controller)

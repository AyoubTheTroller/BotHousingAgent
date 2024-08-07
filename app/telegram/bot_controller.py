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
                 dao_controller_service,
                 scraping_service,
                 event_emitter: EventEmitter,
                 dispatcher: Dispatcher,
                 router_factory: providers.Provider,
                 search_service_factory: providers.Provider):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.logger.info("Initialization Started")
        self.bot = bot
        self.dispatcher = dispatcher
        self.set_dispatcher_dependencies(bot,
                                         event_emitter,
                                         dao_controller_service,
                                         scraping_service,
                                         search_service_factory,
                                         loader_controller,
                                         router_factory)
        self.register_event_emitters()
        self.register_middlewares()
        self.register_handlers()
        self.logger.info("Initialization Completed")

    def set_dispatcher_dependencies(self,
                                    bot,
                                    event_emitter,
                                    dao_controller_service,
                                    scraping_service,
                                    search_service_factory,
                                    loader_controller,
                                    router_factory):
        self.dispatcher["bot"] = bot
        self.dispatcher["event_emitter"] = event_emitter
        self.dispatcher["dao_controller_service"] = dao_controller_service
        self.dispatcher["scraping_service"] = scraping_service
        self.dispatcher["search_service_factory"] = search_service_factory
        self.dispatcher["loader_controller"] = loader_controller
        self.dispatcher["router_factory"] = router_factory

    def register_middlewares(self):
        MiddlewareRegister(self.dispatcher)

    def register_event_emitters(self):
        EventEmitterRegister(self.dispatcher)

    def register_handlers(self):
        AdminRegister(self.dispatcher)
        PresentationRegister(self.dispatcher)
        ConversationRegister(self.dispatcher)
        MenuRegister(self.dispatcher)
        AccountRegister(self.dispatcher)

import logging
from aiogram import Dispatcher, Bot
from dependency_injector import providers
from app.telegram.notification.event_emitter import EventEmitter
from app.telegram.notification.register import EventEmitterRegister
from app.telegram.middleware.register import MiddlewareRegister
from app.telegram.handler.get_search_params.register import SearchParamsRegister
from app.telegram.handler.start.register import StartRegister
from app.telegram.handler.menu.register import MenuRegister
from app.telegram.handler.subscription.register import SubscriptionRegister
from app.telegram.handler.admin.register import AdminRegister

class BotController:

    logger: None

    def __init__(self,
                 bot:Bot,
                 mongo_service,
                 template_service,
                 event_emitter: EventEmitter,
                 dispatcher: Dispatcher,
                 router_factory: providers.Provider):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.logger.info("Initialization Started")
        self.bot: Bot = bot
        self.dispatcher = dispatcher
        self.set_dispatcher_dependencies(event_emitter, mongo_service, template_service)
        self.register_event_emitters()
        self.register_middlewares()
        self.register_handlers(router_factory)
        self.logger.info("Initialization Completed")

    def set_dispatcher_dependencies(self, event_emitter, mongo_service, template_service):
        self.dispatcher["event_emitter"] = event_emitter
        self.dispatcher["mongo_service"] = mongo_service
        self.dispatcher["template_service"] = template_service

    def register_middlewares(self):
        MiddlewareRegister(self.dispatcher)
        self.logger.info("Middlewares Registration Completed")

    def register_event_emitters(self):
        EventEmitterRegister(self.dispatcher, self.bot)
        self.logger.info("EventEmitter Registration Completed")

    def register_handlers(self, router_factory):
        AdminRegister(self.dispatcher, router_factory)
        StartRegister(self.dispatcher, router_factory)
        SearchParamsRegister(self.dispatcher, router_factory)
        MenuRegister(self.dispatcher, router_factory)
        SubscriptionRegister(self.dispatcher, router_factory)
        self.logger.info("Handlers Registration Completed")
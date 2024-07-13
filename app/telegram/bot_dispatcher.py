from aiogram import Dispatcher
from dependency_injector import providers
from app.telegram.middleware.register import MiddlewareRegister
from app.telegram.handler.get_search_params.register import SearchParamsRegister
from app.telegram.handler.start.register import StartRegister
from app.telegram.handler.menu.register import MenuRegister
from app.telegram.handler.subscription.register import SubscriptionRegister
from app.telegram.handler.admin.register import AdminRegister

class BotDispatcher:

    def __init__(self,
                 mongo_service,
                 template_service,
                 dispatcher: Dispatcher,
                 router_factory: providers.Provider):

        self.router_factory = router_factory
        self.dispatcher = dispatcher
        self.dispatcher["mongo_service"] = mongo_service
        self.dispatcher["template_service"] = template_service
        self.initialize_middlewares()
        self.initialize_handlers_register()

    def initialize_middlewares(self):
        MiddlewareRegister(self.dispatcher)
        
    def initialize_handlers_register(self):
        AdminRegister(self.dispatcher, self.router_factory)
        StartRegister(self.dispatcher, self.router_factory)
        SearchParamsRegister(self.dispatcher, self.router_factory)
        MenuRegister(self.dispatcher, self.router_factory)
        SubscriptionRegister(self.dispatcher, self.router_factory)

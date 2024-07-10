from aiogram import Dispatcher
from dependency_injector import providers
from app.telegram.handler.get_search_params.register import SearchParamsRegister

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
        self.initialize_registers()
        
    def initialize_registers(self):
        SearchParamsRegister(self.dispatcher, self.router_factory)

from aiogram import Dispatcher
from dependency_injector import providers
from app.telegram.handler.prepare_url import PrepareUrl

class BotDispatcher:

    def __init__(self,
                 mongo_service,
                 template_service,
                 dispatcher: Dispatcher,
                 router_factory: providers.Provider):
        
        self.mongo_service = mongo_service
        self.template_service = template_service
        self.router_factory = router_factory
        self.dispatcher = dispatcher
        self.initialize_handlers()
        self.set_routers_dispatching()

    def initialize_handlers(self):
        """Initiliazes all handlers from given routers"""
        self.prepare_url = PrepareUrl(self.router_factory(), self.mongo_service,self.template_service)

    def set_routers_dispatching(self):
        """Registers all routers in the bot dispatcher"""
        self.dispatcher.include_routers(
            self.prepare_url.router
        )

import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.handler.subscription.handlers import SubscriptionHandler
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO

class SubscriptionRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader = self.set_loader(dispatcher["template_service"],"user","subscription")
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.register_handlers(dispatcher,router_factory)
        self.logger.info("Registration Completed")
        
    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, interaction_type, handler_type):
        return BaseLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to interact with the user at the start."""
        handler = SubscriptionHandler(self.loader, self.user_dao)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.subscribe, Command(commands=["subscribe"]))
        dispatcher.include_router(handler_router)
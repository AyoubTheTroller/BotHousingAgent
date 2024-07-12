from aiogram import Dispatcher
from aiogram.filters import Command
from app.telegram.handler.loader import Loader
from app.telegram.handler.subscription.handlers import SubscriptionHandler
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user_dao import UserDAO

class SubscriptionRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.dispatcher = dispatcher
        self.router_factory = router_factory
        self.mongo_service: MongoService = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.loader = self.set_loader("user_account","subscription")
        self.user_dao = UserDAO(self.mongo_service.get_telegram_database()["users"])
        self.register_handlers()

    def set_loader(self, interaction_type, handler_type):
        return Loader(self.template_service,interaction_type,handler_type)

    def register_handlers(self):
        """Register scenes that are needed to interact with the user at the start."""
        handler = SubscriptionHandler(self.loader, self.user_dao)
        handler_router = self.router_factory()
        handler_router.message.register(handler.subscribe, Command(commands=["subscribe"]))
        self.dispatcher.include_router(handler_router)
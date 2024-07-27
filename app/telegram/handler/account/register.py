import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.handler.account.handlers import AccountHandler
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.handler.account.handlers import Form

class AccountRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader = self.set_loader(dispatcher["template_service"],"user","account")
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.register_handlers(dispatcher,router_factory, dispatcher["event_emitter"])
        self.logger.info("Registration Completed")
        
    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, interaction_type, handler_type):
        return BaseLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory, event_emitter):
        """Register scenes that are needed to interact with the user at the start."""
        handler = AccountHandler(self.loader, self.user_dao, event_emitter)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.subscribe, Command(commands=["subscribe"]))
        handler_router.message.register(handler.set_language, Command(commands=["set_language"]))
        handler_router.callback_query.register(handler.handle_language, Form.language)
        dispatcher.include_router(handler_router)
import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.handler.admin.handlers import AdminHandler
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO

class AdminRegister:
    def __init__(self,
                 dispatcher: Dispatcher,
                 router_factory):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.regular_user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.admin_user_dao = self.set_user_dao(dispatcher["mongo_service"],"admins")
        self.loader = self.set_loader(dispatcher["template_service"],"user","admin")
        self.register_handlers(dispatcher, router_factory, dispatcher["event_emitter"])
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, interaction_type, handler_type):
        return BaseLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory, event_emitter):
        """Register scenes that are needed to interact with the user at the start."""
        handler = AdminHandler(self.loader, self.regular_user_dao, self.admin_user_dao, event_emitter)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.approve_user, Command(commands=["approve_user"]))
        dispatcher.include_router(handler_router)
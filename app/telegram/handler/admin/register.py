from aiogram import Dispatcher
from aiogram.filters import Command
from app.telegram.notification.event_emitter import EventEmitter
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.handler.admin.handlers import AdminHandler
from app.service.mongodb.mongo_service import MongoService
from app.service.template.template_service import TemplateService
from app.service.mongodb.dao.user.user_dao import UserDAO

class AdminRegister:
    def __init__(self,
                 dispatcher: Dispatcher,
                 router_factory):
        self.dispatcher = dispatcher
        self.router_factory = router_factory
        self.event_emitter: EventEmitter = dispatcher["event_emitter"]
        self.mongo_service: MongoService = dispatcher["mongo_service"]
        self.template_service: TemplateService = dispatcher["template_service"]
        self.regular_user_dao = UserDAO(self.mongo_service.get_telegram_database()["users"])
        self.admin_user_dao = UserDAO(self.mongo_service.get_telegram_database()["admins"])
        self.loader = self.set_loader("user","admin")
        self.register_handlers()

    def set_loader(self, interaction_type, handler_type):
        return BaseLoader(self.template_service,interaction_type,handler_type)

    def register_handlers(self):
        """Register scenes that are needed to interact with the user at the start."""
        handler = AdminHandler(self.loader, self.regular_user_dao, self.admin_user_dao, self.event_emitter)
        handler_router = self.router_factory()
        handler_router.message.register(handler.approve_user, Command(commands=["approve_user"]))
        self.dispatcher.include_router(handler_router)
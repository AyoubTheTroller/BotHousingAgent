import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.telegram.handler.menu.handlers import MenuHandler
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.service.mongodb.mongo_service import MongoService

class MenuRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.loader = self.set_loader(dispatcher["template_service"], "menu", "home")
        self.register_handlers(dispatcher,router_factory)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, interaction_type, handler_type):
        return ComponentsLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register handlers for interactive menu buttons."""
        handler = MenuHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.show_menu, Command(commands=["show_menu"]))
        handler_router.message.register(handler.hide_menu, Command(commands=["hide_menu"]))
        dispatcher.include_router(handler_router)

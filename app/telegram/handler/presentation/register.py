import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.presentation.handlers import StartHandler
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.service.mongodb.mongo_service import MongoService

class PresentationRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory, loader_controller: LoaderController):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader_controller = loader_controller
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.loader = self.set_loader("start")
        self.register_handlers(dispatcher, router_factory)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, handler_type):
        return self.loader_controller.get_loader("presentation",handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to interact with the user at the start."""
        handler = StartHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.start_command, Command(commands=["start"]))
        handler_router.message.register(handler.start_command,F.text=="start")
        dispatcher.include_router(handler_router)

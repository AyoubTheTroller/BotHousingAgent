import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.presentation.handlers import StartHandler
from app.service.mongodb.dao_controller_service import DaoControllerService

class PresentationRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.user_dao = self.set_dao(dispatcher["dao_controller_service"],"users")
        self.loader = self.set_loader(dispatcher["loader_controller"],"start")
        self.register_handlers(dispatcher, dispatcher["router_factory"])
        self.logger.info("Registration Completed")

    def set_dao(self, dao_controller_service: DaoControllerService, collection):
        return dao_controller_service.get_dao("telegram",collection)

    def set_loader(self, loader_controller: LoaderController, handler_type):
        return loader_controller.get_loader("presentation",handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to interact with the user at the start."""
        handler = StartHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.start_command, Command(commands=["start"]))
        handler_router.message.register(handler.start_command,F.text=="start")
        dispatcher.include_router(handler_router)

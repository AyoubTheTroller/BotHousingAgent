import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.menu.handlers import MenuHandler
from app.service.mongodb.dao_controller_service import DaoControllerService

class MenuRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.user_dao = self.set_dao(dispatcher["dao_controller_service"],"users")
        self.loader = self.set_loader(dispatcher["loader_controller"],"home")
        self.register_handlers(dispatcher,dispatcher["router_factory"])
        self.logger.info("Registration Completed")

    def set_dao(self, dao_controller_service: DaoControllerService, collection):
        return dao_controller_service.get_dao("telegram",collection)

    def set_loader(self, loader_controller: LoaderController, handler_type):
        return loader_controller.get_loader("menu",handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register handlers for interactive menu buttons."""
        handler = MenuHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.show_menu, Command(commands=["show_menu"]))
        handler_router.message.register(handler.hide_menu, Command(commands=["hide_menu"]))
        dispatcher.include_router(handler_router)

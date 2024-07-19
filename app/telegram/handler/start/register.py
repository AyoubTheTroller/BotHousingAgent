import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.telegram.handler.start.handlers import StartHandler

class StartRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader = self.set_loader(dispatcher["template_service"], "presentation", "start")
        self.menu_loader = self.set_loader(dispatcher["template_service"], "menu", "home")
        self.register_handlers(dispatcher, router_factory)
        self.logger.info("Registration Completed")

    def set_loader(self, template_service, interaction_type, handler_type):
        return ComponentsLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to interact with the user at the start."""
        handler = StartHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.start_command, Command(commands=["start"]))
        handler_router.message.register(handler.start_command,
                                        F.text==self.menu_loader.get_keyboard_button_template("start"))
        dispatcher.include_router(handler_router)

from aiogram import Dispatcher
from aiogram.filters import Command
from app.telegram.handler.loader import Loader
from app.telegram.handler.menu.handlers import MenuHandler

class MenuRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.dispatcher = dispatcher
        self.router_factory = router_factory
        self.mongo_service = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.loader = self.set_loader("menu","home")
        self.register_handlers()

    def set_loader(self, interaction_type, handler_type):
        return Loader(self.template_service,interaction_type,handler_type)

    def register_handlers(self):
        """Register scenes that are needed to interact with the user at the start."""
        handler = MenuHandler(self.loader)
        handler_router = self.router_factory()
        handler_router.message.register(handler.show_menu, Command(commands=["show_menu"]))
        handler_router.message.register(handler.hide_menu, Command(commands=["hide_menu"]))
        self.dispatcher.include_router(handler_router)

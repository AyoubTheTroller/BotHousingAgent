from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.telegram.handler.menu.handlers import MenuHandler

class MenuRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.loader = self.set_loader(dispatcher["template_service"], "menu", "home")
        self.register_handlers(dispatcher,router_factory)

    def set_loader(self, template_service, interaction_type, handler_type):
        return ComponentsLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register handlers for interactive menu buttons."""
        handler = MenuHandler(self.loader)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.show_menu, Command(commands=["show_menu"]))
        handler_router.message.register(handler.hide_menu, Command(commands=["hide_menu"]))
        dispatcher.include_router(handler_router)

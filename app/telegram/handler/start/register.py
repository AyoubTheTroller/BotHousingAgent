from aiogram import Dispatcher
from aiogram.filters import Command
from app.telegram.handler.loader import Loader
from app.telegram.handler.start.handler import StartHandler

class StartRegister:
    def __init__(self, dispatcher: Dispatcher, router_factory):
        self.dispatcher = dispatcher
        self.router_factory = router_factory
        self.mongo_service = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.loader = self.set_loader()
        self.register_handlers()

    def set_loader(self):
        return Loader(self.mongo_service, self.template_service, "presentation", "start")

    def register_handlers(self):
        """Register scenes that are needed to interact with the user at the start."""
        handler = StartHandler(self.loader)
        handler_router = self.router_factory()
        handler_router.message.register(handler.start_command, Command(commands=["start"]))
        self.dispatcher.include_router(handler_router)

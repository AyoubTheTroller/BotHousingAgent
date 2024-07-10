from aiogram import Dispatcher, F
from aiogram.filters import Command
from app.telegram.handler.get_search_params.loader import Loader
from app.telegram.handler.get_search_params.handlers import Handlers
from app.telegram.handler.get_search_params.handlers import Form

class SearchParamsRegister():

    def __init__(self, dispatcher: Dispatcher, router_factory) -> None:

        self.dispatcher = dispatcher
        self.router_factory = router_factory
        self.mongo_service = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.loader = self.set_loader()
        self.register_handlers()

    def set_loader(self):
        return Loader(self.mongo_service,
                      self.template_service,
                      "conversation",
                      "get_search_params")

    def register_handlers(self):
        """Register scenes that are needed to get search paramans from the user"""
        self.handlers = Handlers(self.loader)
        self.handlers_router = self.router_factory()
        self.handlers_router.message.register(self.handlers.search_house, Command(commands=["search_house"]))
        self.handlers_router.callback_query.register(self.handlers.handle_start, F.data == "start")
        self.handlers_router.message.register(self.handlers.handle_city_name, Form.city_name)
        self.handlers_router.message.register(self.handlers.handle_max_price, Form.max_price)
        self.handlers_router.callback_query.register(self.handlers.handle_appartment_type, Form.appartment_type)
        self.handlers_router.callback_query.register(self.handlers.handle_furnished, Form.furnished)
        self.handlers_router.callback_query.register(self.handlers.handle_confirmation, Form.confirmation)
        self.dispatcher.include_router(self.handlers_router)

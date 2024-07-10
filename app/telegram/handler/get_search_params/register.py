from aiogram import Dispatcher, F
from aiogram.filters import Command
from app.telegram.handler.loader import Loader
from app.telegram.handler.get_search_params.handlers import SearchParamsHandlers
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
        handlers = SearchParamsHandlers(self.loader)
        handlers_router = self.router_factory()
        handlers_router.message.register(handlers.search_house, Command(commands=["search_house"]))
        handlers_router.callback_query.register(handlers.handle_start, F.data == "start")
        handlers_router.message.register(handlers.handle_city_name, Form.city_name)
        handlers_router.message.register(handlers.handle_max_price, Form.max_price)
        handlers_router.callback_query.register(handlers.handle_appartment_type, Form.appartment_type)
        handlers_router.callback_query.register(handlers.handle_furnished, Form.furnished)
        handlers_router.callback_query.register(handlers.handle_confirmation, Form.confirmation)
        self.dispatcher.include_router(handlers_router)

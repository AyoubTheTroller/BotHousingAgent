from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.telegram.handler.get_search_params.handlers import SearchParamsHandlers
from app.telegram.handler.get_search_params.handlers import Form

class SearchParamsRegister():

    def __init__(self, dispatcher: Dispatcher, router_factory) -> None:
        self.conversation_loader = self.set_loader(dispatcher["template_service"], "conversation", "get_search_params")
        self.menu_loader = self.set_loader(dispatcher["template_service"], "menu", "home")
        self.register_handlers(dispatcher, router_factory)

    def set_loader(self, template_service, interaction_type, handler_type):
        return ComponentsLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to get search paramans from the user"""
        handlers = SearchParamsHandlers(self.conversation_loader)
        handlers_router: Router = router_factory()
        handlers_router.message.register(handlers.search_house, Command(commands=["search_house"]))
        handlers_router.message.register(handlers.search_house, F.text == self.menu_loader.get_keyboard_button_template("search_house"))
        handlers_router.callback_query.register(handlers.handle_start, F.data == "start")
        handlers_router.message.register(handlers.handle_city_name, Form.city_name)
        handlers_router.message.register(handlers.handle_max_price, Form.max_price)
        handlers_router.callback_query.register(handlers.handle_appartment_type, Form.appartment_type)
        handlers_router.callback_query.register(handlers.handle_furnished, Form.furnished)
        handlers_router.callback_query.register(handlers.handle_confirmation, Form.confirmation)
        dispatcher.include_router(handlers_router)

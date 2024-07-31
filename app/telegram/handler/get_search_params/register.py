import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.telegram.handler.get_search_params.handlers import SearchParamsHandlers
from app.telegram.handler.get_search_params.handlers import Form
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO

class SearchParamsRegister():

    def __init__(self, dispatcher: Dispatcher, router_factory) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.conversation_loader = self.set_loader(dispatcher["template_service"], "conversation", "get_search_params")
        self.menu_loader = self.set_loader(dispatcher["template_service"], "menu", "home")
        self.register_handlers(dispatcher, router_factory)
        self.logger.info("Registration Completed")
        
    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, interaction_type, handler_type):
        return ComponentsLoader(template_service,interaction_type,handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to get search paramans from the user"""
        handlers = SearchParamsHandlers(self.conversation_loader, dispatcher["scraping_service"])
        handlers_router: Router = router_factory()
        handlers_router.message.register(handlers.search_house, Command(commands=["search_house"]))
        handlers_router.message.register(handlers.search_house, F.text == "search_house")
        handlers_router.callback_query.register(handlers.handle_start, F.data == "start")
        handlers_router.callback_query.register(handlers.handle_go_to_search, F.data == "go_to_search")
        handlers_router.callback_query.register(handlers.handle_skip_step, F.data == "skip_step")
        handlers_router.callback_query.register(handlers.handle_go_prev_step, F.data == "go_prev_step")
        handlers_router.callback_query.register(handlers.handle_search_type, Form.search_type)
        handlers_router.message.register(handlers.handle_location, Form.location)
        handlers_router.message.register(handlers.handle_max_price, Form.max_price)
        handlers_router.callback_query.register(handlers.handle_min_rooms, Form.min_rooms)
        handlers_router.callback_query.register(handlers.handle_max_rooms, Form.max_rooms)
        handlers_router.callback_query.register(handlers.handle_n_bathrooms, Form.n_bathrooms)
        handlers_router.callback_query.register(handlers.handle_furnished, Form.furnished)
        handlers_router.callback_query.register(handlers.handle_balcony, Form.balcony)
        handlers_router.callback_query.register(handlers.handle_terrace, Form.terrace)
        handlers_router.callback_query.register(handlers.handle_pool, Form.pool)
        handlers_router.callback_query.register(handlers.handle_cellar, Form.cellar)
        dispatcher.include_router(handlers_router)

import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.conversation.handlers import SearchParamsHandlers
from app.telegram.handler.conversation.handlers import Form
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO

class ConversationRegister():

    def __init__(self, dispatcher: Dispatcher, router_factory, loader_controller: LoaderController) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader_controller = loader_controller
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"],"users")
        self.conversation_loader = self.set_loader("set_search_params")
        self.search_service = self.set_search_service(dispatcher["search_service_factory"], dispatcher)
        self.register_handlers(dispatcher, router_factory)
        self.logger.info("Registration Completed")
        
    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, handler_type):
        return self.loader_controller.get_loader("conversation",handler_type)
    
    def set_search_service(self, search_service_factory, dispatcher):
        return search_service_factory(dispatcher["scraping_service"],dispatcher["mongo_service"],dispatcher["event_emitter"])

    def register_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to get search paramans from the user"""
        handlers = SearchParamsHandlers(self.conversation_loader, self.search_service)
        handlers_router: Router = router_factory()
        commands = self.conversation_loader.get_base_message_template("commands")
        for command in commands:
            handlers_router.message.register(handlers.set_search_filters, Command(commands=[command]))
        buttons = self.conversation_loader.get_base_button_template("menu_buttons")
        for button in buttons:
            handlers_router.message.register(handlers.set_search_filters, F.text == button)
        handlers_router.callback_query.register(handlers.handle_start, F.data == "start")
        handlers_router.callback_query.register(handlers.handle_go_to_search, F.data == "go_to_search")
        handlers_router.callback_query.register(handlers.handle_skip_step, F.data == "skip_step")
        handlers_router.callback_query.register(handlers.handle_go_prev_step, F.data == "go_prev_step")
        handlers_router.callback_query.register(handlers.start_searching, F.data == "start_searching")
        handlers_router.callback_query.register(handlers.stop_searching, F.data == "stop_searching")
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

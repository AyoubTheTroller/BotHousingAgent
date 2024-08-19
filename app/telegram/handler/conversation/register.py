import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.conversation.handlers.add_search_params import AddSearchParamsHandlers
from app.telegram.handler.conversation.handlers.conversation_states import Form
from app.telegram.handler.conversation.handlers.start_search import StartSearchHandlers
from app.telegram.handler.conversation.handlers.show_search_params import ShowSearchParamsHandlers
from app.service.mongodb.dao_controller_service import DaoControllerService
from app.telegram.notification.event_emitter import EventEmitter

class ConversationRegister():

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.user_dao = self.set_dao(dispatcher["dao_controller_service"],"telegram","users")
        self.search_params_dao = self.set_dao(dispatcher["dao_controller_service"],"scraping","search_params")
        self.add_search_params_loader = self.set_loader(dispatcher["loader_controller"],"add_search_params")
        self.start_search_loader = self.set_loader(dispatcher["loader_controller"],"start_search")
        self.show_search_params_loader = self.set_loader(dispatcher["loader_controller"],"show_search_params")
        self.search_service = self.set_search_service(dispatcher)
        self.register_add_search_params_handlers(dispatcher, dispatcher["router_factory"])
        self.register_start_search_handlers(dispatcher, dispatcher["router_factory"])
        self.register_show_seach_params_handlers(dispatcher, dispatcher["router_factory"])
        self.logger.info("Registration Completed")

    def set_dao(self, dao_controller_service: DaoControllerService, db_key, collection):
        return dao_controller_service.get_dao(db_key,collection)

    def set_loader(self, loader_controller: LoaderController, handler_type):
        return loader_controller.get_loader("conversation",handler_type)
    
    def set_search_service(self, dispatcher):
        return dispatcher["search_service_factory"](event_emitter=dispatcher["event_emitter"],user_dao=self.user_dao,search_params_dao=self.search_params_dao)

    def register_add_search_params_handlers(self, dispatcher: Dispatcher, router_factory):
        """Register scenes that are needed to get search paramans from the user"""
        handlers = AddSearchParamsHandlers(self.add_search_params_loader, self.search_service)
        handlers_router: Router = router_factory()
        commands = self.add_search_params_loader.get_base_message_template("commands")
        for command in commands:
            handlers_router.message.register(handlers.add_search_filters, Command(commands=[command]))
        buttons = self.add_search_params_loader.get_base_button_template("menu_buttons")
        for button in buttons:
            handlers_router.message.register(handlers.add_search_filters, F.text == button)
        handlers_router.callback_query.register(handlers.handle_start, F.data == "start")
        handlers_router.callback_query.register(handlers.handle_review_search_params, F.data == "review_params")
        handlers_router.callback_query.register(handlers.handle_skip_step, F.data == "skip_step")
        handlers_router.callback_query.register(handlers.handle_go_prev_step, F.data == "go_prev_step")
        handlers_router.callback_query.register(handlers.handle_save_search_params, F.data == "save_search_params")
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
        handlers_router.message.register(handlers.handle_custom_name, Form.custom_name)
        dispatcher.include_router(handlers_router)
        ## Register custom event emitter
        self.register_message_event(dispatcher["event_emitter"],"add_search_filters",handlers.add_search_filters)

    def register_start_search_handlers(self, dispatcher: Dispatcher, router_factory):
        handlers = StartSearchHandlers(self.start_search_loader,self.search_service)
        handlers_router: Router = router_factory()
        handlers_router.message.register(handlers.start_home_search, Command(commands=["start_home_search"]))
        handlers_router.message.register(handlers.stop_search_with_command, Command(commands=["stop_search"]))
        handlers_router.callback_query.register(handlers.start_search_with_callback, F.data == "start_search")
        handlers_router.callback_query.register(handlers.stop_search_with_callback, F.data == "stop_search")
        handlers_router.callback_query.register(handlers.use_new_filters, F.data == "use_new_filters")
        handlers_router.callback_query.register(handlers.start_search_using_filters, F.data.startswith("start_search_using_filters"))
        dispatcher.include_router(handlers_router)

    def register_show_seach_params_handlers(self, dispatcher: Dispatcher, router_factory):
        handlers = ShowSearchParamsHandlers(self.show_search_params_loader,self.search_service)
        handlers_router: Router = router_factory()
        handlers_router.message.register(handlers.show_saved_filters_command, Command(commands=["show_search_filters"]))
        handlers_router.callback_query.register(handlers.show_saved_filters_callback, F.data == "show_saved_filters")
        handlers_router.callback_query.register(handlers.remove_search_params, F.data.startswith("remove_search_filters_"))
        handlers_router.callback_query.register(handlers.handle_delete_filters, F.data.startswith("delete_filters"))
        handlers_router.callback_query.register(handlers.handle_keep_filters, F.data == ("keep_filters"))
        dispatcher.include_router(handlers_router)

    def register_callback_query_event(self, event_emitter: EventEmitter, event_type, handler):
        event_emitter.on_callback_query(event_type,handler)

    def register_message_event(self, event_emitter: EventEmitter, event_type, handler):
        event_emitter.on_message(event_type,handler)

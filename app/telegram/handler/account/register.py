import logging
from aiogram import Dispatcher, Router
from aiogram.filters import Command
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.handler.account.handlers import AccountHandler
from app.service.mongodb.dao_controller_service import DaoControllerService
from app.telegram.handler.account.handlers import Form

class AccountRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader = self.set_loader(dispatcher["loader_controller"],"account")
        self.user_dao = self.set_dao(dispatcher["dao_controller_service"],"users")
        self.register_handlers(dispatcher,dispatcher["router_factory"], dispatcher["event_emitter"])
        self.logger.info("Registration Completed")

    def set_dao(self, dao_controller_service: DaoControllerService, collection):
        return dao_controller_service.get_dao("telegram",collection)

    def set_loader(self, loader_controller: LoaderController, handler_type):
        return loader_controller.get_loader("user",handler_type)

    def register_handlers(self, dispatcher: Dispatcher, router_factory, event_emitter):
        """Register scenes that are needed to interact with the user at the start."""
        handler = AccountHandler(self.loader, self.user_dao, event_emitter)
        handler_router: Router = router_factory()
        handler_router.message.register(handler.subscribe, Command(commands=["subscribe"]))
        handler_router.message.register(handler.set_language, Command(commands=["set_language"]))
        handler_router.callback_query.register(handler.handle_language, Form.language)
        dispatcher.include_router(handler_router)
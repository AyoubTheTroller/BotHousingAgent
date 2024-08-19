import logging
from aiogram import Dispatcher
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.dao_controller_service import DaoControllerService
from app.telegram.notification.triggered.base_events import BaseTriggeredNotificationEvent
from app.telegram.notification.triggered.admin_events import AdminTriggeredNotificationEvent
from app.telegram.notification.triggered.search_events import SearchEvents

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.base_loader = self.set_loader(dispatcher["loader_controller"],"base")
        self.admin_loader = self.set_loader(dispatcher["loader_controller"],"admin")
        self.search_loader = self.set_loader(dispatcher["loader_controller"],"search_hub")
        self.user_dao = self.set_dao(dispatcher["dao_controller_service"],"users")
        self.admin_dao = self.set_dao(dispatcher["dao_controller_service"],"admins")
        self.register_triggered_events(dispatcher["event_emitter"],dispatcher["bot"])
        self.logger.info("Registration Completed")

    def set_dao(self, dao_controller_service: DaoControllerService, collection):
        return dao_controller_service.get_dao("telegram",collection)

    def set_loader(self, loader_controller: LoaderController, handler_type):
        return loader_controller.get_loader("notification",handler_type)

    def register_triggered_events(self, event_emitter: EventEmitter, bot):
        """Register scenes that are needed to interact with the user at the start."""
        base_triggerd_events = BaseTriggeredNotificationEvent(self.base_loader, self.user_dao, bot)
        event_emitter.on("user_approved",base_triggerd_events.user_approved)
        admin_triggerd_events = AdminTriggeredNotificationEvent(self.admin_loader, self.admin_dao, bot)
        event_emitter.on("new_user_subscription",admin_triggerd_events.new_user_subscription)
        search_events = SearchEvents(self.search_loader, self.user_dao, bot)
        event_emitter.on("prepare_for_search", search_events.prepare_for_search)
        event_emitter.on("new_listing_found", search_events.new_listing_found)
        event_emitter.on("no_listings_found", search_events.no_listings_found)
        event_emitter.on("stop_search", search_events.stop_search)
        event_emitter.on("search_completed", search_events.search_completed)

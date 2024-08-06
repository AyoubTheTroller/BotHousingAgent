import logging
from aiogram import Bot, Dispatcher
from app.telegram.loader.loader_controller import LoaderController
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.notification.triggered.base_events import BaseTriggeredNotificationEvent
from app.telegram.notification.triggered.admin_events import AdminTriggeredNotificationEvent

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher, bot: Bot, loader_controller: LoaderController):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader_controller = loader_controller
        self.base_loader = self.set_loader("base")
        self.admin_loader = self.set_loader("admin")
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"], "users")
        self.admin_dao = self.set_user_dao(dispatcher["mongo_service"], "admins")
        self.register_triggered_events(dispatcher["event_emitter"], bot)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, handler_type):
        return self.loader_controller.get_loader("notification",handler_type)

    def register_triggered_events(self, event_emitter: EventEmitter, bot):
        """Register scenes that are needed to interact with the user at the start."""
        base_triggerd_events = BaseTriggeredNotificationEvent(self.base_loader, self.user_dao, bot)
        event_emitter.on("user_approved",base_triggerd_events.user_approved)
        admin_triggerd_events = AdminTriggeredNotificationEvent(self.admin_loader, self.admin_dao, bot)
        event_emitter.on("new_user_subscription",admin_triggerd_events.new_user_subscription)

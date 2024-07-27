import logging
from aiogram import Bot, Dispatcher
from app.telegram.notification.loader import NotificationLoader
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.notification.triggered.base_events import TriggeredNotificationEvent
from app.telegram.notification.triggered.admin_events import AdminTriggeredNotificationEvent

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.base_loader = self.set_loader(dispatcher["template_service"], "base")
        self.admin_loader = self.set_loader(dispatcher["template_service"], "admin")
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"], "users")
        self.admin_dao = self.set_user_dao(dispatcher["mongo_service"], "admins")
        self.register_triggered_events(dispatcher["event_emitter"], bot)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, handler_type):
        return NotificationLoader(template_service,"notification",handler_type)

    def register_triggered_events(self, event_emitter: EventEmitter, bot):
        """Register scenes that are needed to interact with the user at the start."""
        base_triggerd_events = TriggeredNotificationEvent(self.base_loader, self.user_dao, bot)
        event_emitter.on("user_approved",base_triggerd_events.user_approved)
        admin_triggerd_events = AdminTriggeredNotificationEvent(self.admin_loader, self.admin_dao, bot)
        event_emitter.on("new_user_subscription",admin_triggerd_events.new_user_subscription)

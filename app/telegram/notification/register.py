import logging
from aiogram import Bot, Dispatcher
from app.telegram.notification.loader import NotificationLoader
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.notification.triggered.base_events import TriggeredNotificationEvent

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader = self.set_loader(dispatcher["template_service"], "base")
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"], "users")
        self.register_triggered_events(dispatcher["event_emitter"], bot)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, template_service, handler_type):
        return NotificationLoader(template_service,"notification",handler_type)

    def register_triggered_events(self, event_emitter: EventEmitter, bot):
        """Register scenes that are needed to interact with the user at the start."""
        triggerd_events = TriggeredNotificationEvent(self.loader, self.user_dao, bot)
        event_emitter.on("user_approved",triggerd_events.user_approved)

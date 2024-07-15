from aiogram import Bot, Dispatcher
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.notification.event_emitter import EventEmitter
from app.telegram.notification.triggered.base_events import TriggeredNotificationEvent

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.bot = bot
        self.dispatcher = dispatcher
        self.event_emitter: EventEmitter = self.dispatcher["event_emitter"]
        self.template_service = self.dispatcher["template_service"]
        self.mongo_service = self.dispatcher["mongo_service"]
        self.base_loader = self.set_loader("base")
        self.register_triggered_events()

    def set_loader(self, handler_type):
        return BaseLoader(self.template_service,"notification",handler_type)

    def register_triggered_events(self):
        """Register scenes that are needed to interact with the user at the start."""
        triggerd_events = TriggeredNotificationEvent(self.base_loader, self.bot)
        self.event_emitter.on("user_approved",triggerd_events.user_approved)

from aiogram import Bot, Dispatcher
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.notification.event_emitter import EventEmitter
from app.telegram.notification.triggered.base_events import TriggeredNotificationEvent

class EventEmitterRegister:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.base_loader = self.set_loader(dispatcher["template_service"], "base")
        self.register_triggered_events(dispatcher["event_emitter"], bot)

    def set_loader(self, template_service, handler_type):
        return BaseLoader(template_service,"notification",handler_type)

    def register_triggered_events(self, event_emitter: EventEmitter, bot):
        """Register scenes that are needed to interact with the user at the start."""
        triggerd_events = TriggeredNotificationEvent(self.base_loader, bot)
        event_emitter.on("user_approved",triggerd_events.user_approved)

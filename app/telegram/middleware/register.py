from aiogram import Dispatcher
from app.telegram.handler.loader import Loader
from app.telegram.middleware.rate_limiter.max_messages import RateLimitMiddleware

class MiddlewareRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.mongo_service = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.rate_limit_loader = self.set_loader("ratelimiter")
        self.register_message_middlewares()

    def set_loader(self, handler_type):
        return Loader(self.template_service,"middlewares",handler_type)

    def register_message_middlewares(self):
        """Register scenes that are needed to interact with the user at the start."""
        self.dispatcher.message.middleware(RateLimitMiddleware(self.rate_limit_loader))
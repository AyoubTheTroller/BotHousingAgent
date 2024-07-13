from aiogram import Dispatcher
from app.service.mongodb.mongo_service import MongoService
from app.telegram.handler.loader.base_loader import BaseLoader
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.middleware.rate_limiter.max_messages import RateLimitMiddleware
from app.telegram.middleware.authorization.auth import AuthorizationMiddleware

class MiddlewareRegister:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.mongo_service: MongoService = dispatcher["mongo_service"]
        self.template_service = dispatcher["template_service"]
        self.user_dao = UserDAO(self.mongo_service.get_telegram_database()["users"])
        self.rate_limit_loader = self.set_loader("ratelimiter")
        self.authorization_loader = self.set_loader("authorization")
        self.register_message_middlewares()

    def set_loader(self, handler_type):
        return BaseLoader(self.template_service,"middlewares",handler_type)

    def register_message_middlewares(self):
        """Register scenes that are needed to interact with the user at the start."""
        self.dispatcher.message.middleware(RateLimitMiddleware(self.rate_limit_loader))
        self.dispatcher.message.middleware(AuthorizationMiddleware(self.authorization_loader, self.user_dao))
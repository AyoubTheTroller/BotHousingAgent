from aiogram import Dispatcher
from app.service.mongodb.mongo_service import MongoService
from app.telegram.handler.loader.base_loader import BaseLoader
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.middleware.rate_limiter.max_messages import RateLimitMiddleware
from app.telegram.middleware.authorization.auth import AuthorizationMiddleware

class MiddlewareRegister:
    def __init__(self, dispatcher):
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"], "users")
        self.rate_limit_loader = self.set_loader("ratelimiter", dispatcher["template_service"])
        self.authorization_loader = self.set_loader("authorization", dispatcher["template_service"])
        self.register_message_middlewares(dispatcher)

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, handler_type, template_service):
        return BaseLoader(template_service,"middlewares",handler_type)

    def register_message_middlewares(self, dispatcher: Dispatcher):
        """Register scenes that are needed to interact with the user at the start."""
        dispatcher.message.middleware(RateLimitMiddleware(self.rate_limit_loader))
        dispatcher.message.middleware(AuthorizationMiddleware(self.authorization_loader, self.user_dao))

import logging
from aiogram import Dispatcher
from app.telegram.loader.loader_controller import LoaderController
from app.service.mongodb.mongo_service import MongoService
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.middleware.exception.exception import ExceptionMiddleware
from app.telegram.middleware.rate_limiter.max_messages import RateLimitMiddleware
from app.telegram.middleware.authorization.auth import AuthorizationMiddleware
from app.telegram.middleware.state.session_state import SessionStateMiddleware
from app.telegram.middleware.state.conversation_state import ConversationStateMiddleware

class MiddlewareRegister:
    def __init__(self, dispatcher, loader_controller: LoaderController):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.loader_controller = loader_controller
        self.user_dao = self.set_user_dao(dispatcher["mongo_service"], "users")
        self.rate_limit_loader = self.set_loader("ratelimiter")
        self.authorization_loader = self.set_loader("authorization")
        self.exception_loader = self.set_loader("exception")
        self.state_loader = self.set_loader("state")
        self.register_middlewares(dispatcher)
        self.logger.info("Registration Completed")

    def set_user_dao(self, mongo_service: MongoService, collection) -> UserDAO:
        return UserDAO(mongo_service.get_telegram_database()[collection])

    def set_loader(self, handler_type):
        return self.loader_controller.get_loader("middlewares",handler_type)

    def register_middlewares(self, dispatcher: Dispatcher):
        """Register middlewares for messages and callback queries"""
        exception_middleware = ExceptionMiddleware(self.exception_loader)
        dispatcher.message.middleware(exception_middleware)
        dispatcher.callback_query.middleware(exception_middleware)

        rate_limit_middleware = RateLimitMiddleware(self.rate_limit_loader)
        dispatcher.message.middleware(rate_limit_middleware)
        dispatcher.callback_query.middleware(rate_limit_middleware)

        authorization_middleware = AuthorizationMiddleware(self.authorization_loader, self.user_dao)
        dispatcher.message.middleware(authorization_middleware)
        dispatcher.callback_query.middleware(authorization_middleware)

        conversation_state_middleware = ConversationStateMiddleware(self.state_loader)
        dispatcher.message.middleware(conversation_state_middleware)
        dispatcher.callback_query.middleware(conversation_state_middleware)

        session_state_middleware = SessionStateMiddleware(self.user_dao)
        dispatcher.message.middleware(session_state_middleware)
        dispatcher.callback_query.middleware(session_state_middleware)

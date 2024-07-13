# authorization_middleware.py
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.handler.loader.base_loader import BaseLoader

class AuthorizationMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader, user_dao: UserDAO):
        self.user_dao = user_dao
        self.loader = loader

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        user = await self.user_dao.get_user_by_id(user_id)

        if user and user.authorized:
            return await handler(event, data)
        else:
            await event.answer(self.loader.get_message_template("not_authorized"))

from datetime import datetime
from aiogram.types import Message
from app.telegram.handler.loader import Loader
from app.telegram.model.user import User
from app.service.mongodb.dao.user_dao import UserDAO

class SubscriptionHandler:
    def __init__(self, loader: Loader, user_dao: UserDAO):
        self.loader = loader
        self.user_dao = user_dao

    async def subscribe(self, message: Message):
        user_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "authorized": True,
            "created_at": datetime.now(),
            "last_active": datetime.now()
        }
        user = User(**user_data)
        await self.user_dao.add_user(user)
        await message.answer(self.loader.get_message_template("welcome",username=message.from_user.username))
# handlers.py
from datetime import datetime
from aiogram.types import Message
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.model.user import User
from app.service.mongodb.dao.user.user_dao import UserDAO

class SubscriptionHandler:
    def __init__(self, loader: BaseLoader, user_dao: UserDAO):
        self.loader = loader
        self.user_dao = user_dao

    async def subscribe(self, message: Message):
        user_id = message.from_user.id
        existing_user = await self.user_dao.get_user_by_id(user_id)

        if existing_user:
            if existing_user.authorized:
                await message.answer(self.loader.get_message_template("already_subscribed", username=message.from_user.username))
            else:
                await message.answer(self.loader.get_message_template("awaiting_approval", username=message.from_user.username))
        else:
            user_data = {
                "user_id": user_id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "authorized": False,  # Set authorization to false initially
                "created_at": datetime.now(),
                "last_active": datetime.now()
            }
            user = User(**user_data)
            await self.user_dao.add_user(user)
            await message.answer(self.loader.get_message_template("awaiting_approval", username=message.from_user.username))

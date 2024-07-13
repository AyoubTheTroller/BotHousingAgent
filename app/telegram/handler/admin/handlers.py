from aiogram.types import Message
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.handler.loader.base_loader import BaseLoader

class AdminHandler:
    def __init__(self, loader:BaseLoader, regular_user_dao: UserDAO, admin_user_dao: UserDAO):
        self.loader = loader
        self.regular_user_dao = regular_user_dao
        self.admin_user_dao = admin_user_dao

    async def approve_user(self, message: Message):
        user_id = message.from_user.id
        existing_admin_user = await self.admin_user_dao.get_user_by_id(user_id)
        if existing_admin_user.authorized:
            username = message.text.split()[1].lstrip('@')
            user = await self.regular_user_dao.get_user_by_username(username)
            if user:
                if not user.authorized:
                    await self.regular_user_dao.update_user_authorization(user.user_id, True)
                    await message.answer(self.loader.get_message_template("user_approved",username=username))
                elif user.authorized:
                    await message.answer(self.loader.get_message_template("user_already_approved",username=username))
            else:
                await message.answer(self.loader.get_message_template("user_not_found",username=username))
        else:
            await message.answer(self.loader.get_message_template("not_authorized"))

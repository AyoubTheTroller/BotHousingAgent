from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.notification.event_emitter import EventEmitter

class AdminHandler:
    def __init__(self,
                 loader:BaseLoader,
                 regular_user_dao: UserDAO,
                 admin_user_dao: UserDAO,
                 event_emitter: EventEmitter):
        self.loader = loader
        self.regular_user_dao = regular_user_dao
        self.admin_user_dao = admin_user_dao
        self.event_emitter = event_emitter

    async def approve_user(self, message: Message, state:FSMContext):
        user_id = message.from_user.id
        existing_admin_user = await self.admin_user_dao.get_user_by_id(user_id)
        if existing_admin_user.authorized:
            username = message.text.split()[1].lstrip('@')
            user = await self.regular_user_dao.get_user_by_username(username)
            if user:
                if not user.authorized:
                    await self.regular_user_dao.update_user_authorization(user.user_id, True)
                    await message.answer(await self.loader.get_message_template("user_approved", state, username=username))
                    await self.event_emitter.emit(
                        event_type="user_approved",
                        event_data={
                            "user_id": user.user_id,
                            "admin_username": existing_admin_user.username
                        }
                    )
                elif user.authorized:
                    await message.answer(await self.loader.get_message_template("user_already_approved", state, username=username))
            else:
                await message.answer(await self.loader.get_message_template("user_not_found", state, username=username))
        else:
            await message.answer(await self.loader.get_message_template("not_authorized", state))

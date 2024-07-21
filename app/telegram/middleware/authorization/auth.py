from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.handler.loader.base_loader import BaseLoader

class AuthorizationMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader, user_dao: UserDAO, session_time = 5):
        self.user_dao = user_dao
        self.loader = loader
        self.session_time = session_time

    async def __call__(self, handler, event: Message, data: dict):
        if isinstance(event, Message):
            if event.text and event.text.startswith("/subscribe"):
                return await handler(event, data)
        user_id = event.from_user.id
        state: FSMContext = data.get('state')

        user = await self.user_dao.get_user_by_id(user_id)
        if user and user.authorized:
            return await handler(event, data)
        else:
            await event.answer(await self.loader.get_message_template("not_authorized", state))
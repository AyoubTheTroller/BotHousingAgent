# handlers.py
from datetime import datetime
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.model.user import User
from app.service.mongodb.dao.user.user_dao import UserDAO

class Form(StatesGroup):
    language = State()

class AccountHandler:
    def __init__(self, loader: BaseLoader, user_dao: UserDAO):
        self.loader = loader
        self.user_dao = user_dao

    async def subscribe(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        existing_user = await self.user_dao.get_user_by_id(user_id)

        if existing_user:
            if existing_user.authorized:
                await message.answer(await self.loader.get_message_template("already_subscribed", state, username=message.from_user.username))
            else:
                await message.answer(await self.loader.get_message_template("awaiting_approval", state, username=message.from_user.username))
        else:
            user_data = {
                "user_id": user_id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "authorized": False,
                "created_at": datetime.now(),
                "last_active": datetime.now(),
                "language":"it"
            }
            user = User(**user_data)
            await self.user_dao.add_user(user)
            await message.answer(await self.loader.get_message_template("awaiting_approval", state, username=message.from_user.username))

    async def set_language(self, message: Message, state: FSMContext):
        await state.set_state(Form.language)
        buttons = await self.loader.get_keyboard_button_template("languages", state)
        buttons_tuples = [(text.split('-')[0], text.split('-')[1]) for text in buttons]
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup(buttons_tuples)
        await message.answer(await self.loader.get_message_template("set_language", state),reply_markup=keyboard_markup)

    async def handle_language(self, callback_query: CallbackQuery, state: FSMContext):
        user_id = callback_query.from_user.id
        await self.user_dao.update_user_language(user_id, callback_query.data)
        await state.update_data(language=callback_query.data)
        await callback_query.message.answer(await self.loader.get_message_template("language_updated",state))
from datetime import datetime
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.telegram.loader.components_loader import ComponentsLoader
from app.telegram.model.user import User
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.notification.event_emitter import EventEmitter
from app import config_var

class Form(StatesGroup):
    language = State()
    end = State()

class AccountHandler:
    def __init__(self, loader: ComponentsLoader, user_dao: UserDAO, event_emitter: EventEmitter):
        self.loader = loader
        self.user_dao = user_dao
        self.event_emitter = event_emitter


    async def subscribe(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        existing_user = await self.user_dao.get_user_by_id(user_id)
        priority_username = message.from_user.username or message.from_user.first_name or message.from_user.last_name

        if existing_user:
            if existing_user.authorized:
                await message.answer(await self.loader.get_message_template(state, "already_subscribed", username=priority_username))
            else:
                await message.answer(await self.loader.get_message_template(state, "awaiting_approval", username=priority_username))
        else:
            user_data = {
                "id": user_id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "authorized": False,
                "created_at": datetime.now(),
                "last_active": datetime.now(),
                "language":"it"
            }
            event_data={
                "admin_username": config_var.sys_admin_username
            }
            user = User(**user_data)
            await self.user_dao.add_user(user)
            event_data["id"] = message.from_user.id
            event_data["username"] = message.from_user.username
            event_data["first_name"] = message.from_user.first_name
            event_data["last_name"] = message.from_user.last_name
            await message.answer(await self.loader.get_message_template(state, "awaiting_approval", username=priority_username))
            await self.event_emitter.emit(
                event_type="new_user_subscription",
                event_data=event_data
            )

    async def set_language(self, message: Message, state: FSMContext):
        await state.set_state(Form.language)
        buttons = await self.loader.get_keyboard_button_template(state, "languages")
        buttons_tuples = [(text.split('-')[0], text.split('-')[1]) for text in buttons]
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup(buttons_tuples)
        await message.answer(await self.loader.get_message_template(state, "set_language"),reply_markup=keyboard_markup)

    async def handle_language(self, callback_query: CallbackQuery, state: FSMContext):
        user_id = callback_query.from_user.id
        await self.user_dao.update_user_language(user_id, callback_query.data)
        await state.update_data(language=callback_query.data)
        await callback_query.message.answer(await self.loader.get_message_template(state, "language_updated"))
        await state.set_state(Form.end)

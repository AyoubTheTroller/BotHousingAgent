from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from app.telegram.loader.base_loader import BaseLoader

class Form(StatesGroup):
    end = State()


class ConversationStateMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader, session_time = 5):
        self.loader = loader
        self.session_time = session_time

    async def __call__(self, handler, event, data: dict):
        state: FSMContext = data.get('state')

        if isinstance(event, Message) and event.text.startswith("/"):
            # If it's a command, clear the state to start a new conversation
            await state.clear()
            return await handler(event, data)

        if isinstance(event, (Message, CallbackQuery)):
            current_state = await state.get_state()
            if current_state == Form.end:
                if isinstance(event, Message):
                    await event.answer(await self.loader.get_message_template(state, "start_over"))
                elif isinstance(event, CallbackQuery):
                    await event.answer(await self.loader.get_message_template(state, "start_over"))
                return
        
        return await handler(event, data)
    
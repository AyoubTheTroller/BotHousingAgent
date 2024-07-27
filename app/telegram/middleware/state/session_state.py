from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from app.service.mongodb.dao.user.user_dao import UserDAO

class Form(StatesGroup):
    end = State()

class SessionStateMiddleware(BaseMiddleware):
    def __init__(self, user_dao: UserDAO, session_time = 5):
        self.user_dao = user_dao
        self.session_time = session_time

    async def __call__(self, handler, event: Message, data: dict):
        state: FSMContext = data.get('state')
        user_data = await state.get_data()
        last_logged = user_data.get('logged')
        current_time = datetime.now()
        if last_logged:
            last_logged_time = datetime.fromisoformat(last_logged)
            if current_time - last_logged_time < timedelta(self.session_time):
                return await handler(event, data)
        
        user_id = event.from_user.id
        user = await self.user_dao.get_user_by_id(user_id)
        if user:
            data['language'] = user.language
            await state.update_data(language=user.language, logged=current_time.isoformat())
        
        return await handler(event, data)
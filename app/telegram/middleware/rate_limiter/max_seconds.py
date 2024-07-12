import time
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.telegram.middleware.loader import Loader

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, loader: Loader, rate_limit: int = 5):
        self.rate_limit = rate_limit
        self.users_last_message_time = defaultdict(lambda: 0)
        self.loader = loader

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()

        if current_time - self.users_last_message_time[user_id] < self.rate_limit:
            self.users_last_message_time[user_id] = current_time
            await event.answer(self.loader.get_message_template("max_seconds"))
        else:
            self.users_last_message_time[user_id] = current_time
            return await handler(event, data)

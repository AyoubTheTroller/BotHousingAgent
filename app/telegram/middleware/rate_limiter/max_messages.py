import time
from collections import defaultdict, deque
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.telegram.middleware.loader import Loader

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, loader: Loader, message_limit: int = 5, window_size: int = 60):
        self.message_limit = message_limit  # Max number of messages allowed
        self.window_size = window_size  # Time window in seconds
        self.user_messages = defaultdict(lambda: deque())
        self.loader = loader

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()

        # Get the deque of message times for the user
        message_times = self.user_messages[user_id]

        # Remove messages that are outside the time window
        while message_times and message_times[0] < current_time - self.window_size:
            message_times.popleft()

        # Check if the user has exceeded the message limit
        if len(message_times) >= self.message_limit:
            await event.answer(self.loader.get_message_template("max_messages"))
        else:
            # Add the current message time to the deque
            message_times.append(current_time)
            return await handler(event, data)

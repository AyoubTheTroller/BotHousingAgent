import logging
from aiogram.types import Update, Message, CallbackQuery

class ErrorHandler:
    def __init__(self, default_error):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.default_error = default_error
        self.error_message_handlers = {}

    def register_message_handler(self, error_type, handler):
        self.error_message_handlers[error_type] = handler

    async def handle(self, error, event, state, **kwargs):
        error_type = type(error)
        handler = self.error_message_handlers.get(error_type, self.default_error)
        error_message = await handler(error, state, **kwargs)
        if error_message != {}:
            await self.send_error_message(event, error_message)
        else:
            await self.send_error_message(event, await self.default_error(error, state, **kwargs))
        self.logger.error(error_message)

    async def send_error_message(self, event, response_message: str):
        if isinstance(event, CallbackQuery):
            await self.handle_message_event(event, response_message)
        elif isinstance(event, Message):
            await self.handle_callback_query_event(event, response_message)
        elif isinstance(event, Update):
            if event.message:
                await self.handle_message_event(event.message, response_message)
            elif event.callback_query:
                await self.handle_callback_query_event(event.callback_query, response_message)
        else:
            self.logger.error("Unhandled event type: %s",type(event))

    async def handle_message_event(self, message: Message, response_message):
        await message.answer(response_message)

    async def handle_callback_query_event(self, callback_query: CallbackQuery, response_message):
        await callback_query.answer(response_message)

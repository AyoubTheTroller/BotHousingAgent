import logging
from aiogram.types import Update
from app.telegram.handler.loader.base_loader import BaseLoader

class GenericErrorHandler:
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.loader = loader
        self.error_handlers = {}

    def register_error_handler(self, error_type, handler):
        self.error_handlers[error_type] = handler

    async def handle(self, error, event, state):
        error_type = type(error)
        handler = self.error_handlers.get(error_type, self.default_handler)
        await handler(error, event, state)

    async def default_handler(self, error, event: Update, state):
        error_message = f"Unhandled exception: {str(error)}"
        self.logger.error(error_message)
        if event.message:
            await event.message.answer(await self.loader.get_message_template(state, "generic_error", "generic"))

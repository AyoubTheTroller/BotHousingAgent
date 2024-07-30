from aiogram.exceptions import TelegramAPIError
from aiogram.types import Update
from app.telegram.middleware.exception.generic.error_handler import GenericErrorHandler
from app.telegram.handler.loader.base_loader import BaseLoader

class TelegramErrorHandler:
    def __init__(self, loader: BaseLoader, generic_handler: GenericErrorHandler):
        self.loader = loader
        self.generic_handler = generic_handler
        self.logger = self.generic_handler.logger

        # Register specific error handler for Telegram API errors
        self.generic_handler.register_error_handler(TelegramAPIError, self.handle_telegram_api_error)

    async def handle_telegram_api_error(self, error: TelegramAPIError, event: Update, state):
        message = f"Telegram API error: {str(error)}"
        self.logger.error(message)
        await event.message.answer(await self.loader.get_message_template(state, "telegram_error", "generic"))

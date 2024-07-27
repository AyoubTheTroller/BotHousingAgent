import logging
import traceback
from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.base_loader import BaseLoader

class ExceptionMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.loader: BaseLoader = loader

    async def __call__(self, handler, event: Update, data: dict):
        state: FSMContext = data.get('state')
        try:
            return await handler(event, data)
        except TelegramAPIError as e:
            error_message = f"Telegram API error: {str(e)}"
            self.logger.error(error_message)
            self.logger.error(traceback.format_exc())
            if event.message:
                await event.message.answer(await self.loader.get_message_template("telegram_error", state))
        except Exception as e:
            error_message = f"Unhandled exception: {str(e)}"
            self.logger.error(error_message)
            self.logger.error(traceback.format_exc())
            if event.message:
                await event.message.answer(await self.loader.get_message_template("generic_error", state))

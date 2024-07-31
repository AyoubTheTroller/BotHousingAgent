import logging
import traceback
from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.generic.error_handler import GenericErrorHandler
from app.telegram.middleware.exception.httpclient.error_handler import HttpClientErrorHandler
from app.telegram.middleware.exception.telegram.error_handler import TelegramErrorHandler

class ExceptionMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.loader: BaseLoader = loader
        self.generic_error_handler = GenericErrorHandler(loader)
        self.http_client_error_handler = HttpClientErrorHandler(loader, self.generic_error_handler)
        self.telegram_error_handler = TelegramErrorHandler(loader, self.generic_error_handler)


    async def __call__(self, handler, event: Update, data: dict):
        state: FSMContext = data.get('state')
        try:
            return await handler(event, data)
        except Exception as e:
            await self.generic_error_handler.handle(e, event, state)
            self.logger.error(traceback.format_exc())

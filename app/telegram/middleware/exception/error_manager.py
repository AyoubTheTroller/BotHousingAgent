import logging
from aiohttp.client_exceptions import ClientError
from aiogram.exceptions import TelegramAPIError
from app.telegram.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.error_handler import ErrorHandler
from app.telegram.middleware.exception.generic.error_handler import GenericErrorHandler
from app.telegram.middleware.exception.http_client.error_handler import HttpClientErrorHandler
from app.telegram.middleware.exception.telegram.error_handler import TelegramErrorHandler

class ErrorManager:
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.loader = loader
        self.error_handlers = {}

    def register_error_handlers(self):
        self.error_handlers[Exception] = GenericErrorHandler(self.loader)
        self.error_handlers[ClientError] = HttpClientErrorHandler(self.loader)
        self.error_handlers[TelegramAPIError] = TelegramErrorHandler(self.loader)

    async def handle_error(self, error, event, state, **kwargs):
        error_type = type(error)
        handler: ErrorHandler = self.error_handlers.get(error_type, self.error_handlers[Exception])
        await handler.handle(error, event, state, **kwargs)
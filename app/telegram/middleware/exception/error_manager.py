import logging
from aiohttp.client_exceptions import ClientError
from aiogram.exceptions import TelegramAPIError
from app.telegram.middleware.exception.dao_operations.custom_exceptions import DaoError
from app.telegram.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.error_handler import ErrorHandler
from app.telegram.middleware.exception.generic.error_handler import GenericErrorHandler
from app.telegram.middleware.exception.http_client.error_handler import HttpClientErrorHandler
from app.telegram.middleware.exception.telegram.error_handler import TelegramErrorHandler
from app.telegram.middleware.exception.dao_operations.error_handler import DaoErrorHandler

class ErrorManager:
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.loader = loader
        self.error_handlers = {}
        self.generic_error_handler = GenericErrorHandler(self.loader)

    def register_error_handlers(self):
        self.error_handlers[ClientError] = HttpClientErrorHandler(self.loader)
        self.error_handlers[TelegramAPIError] = TelegramErrorHandler(self.loader)
        self.error_handlers[DaoError] = DaoErrorHandler(self.loader)

    async def handle_error(self, error, event, state, **kwargs):
        error_type = type(error)
        handler: ErrorHandler = None
        for registered_error, registered_handler in self.error_handlers.items():
            if issubclass(error_type, registered_error):
                handler = registered_handler
                break

        if handler is None:
            handler = self.generic_error_handler

        await handler.handle(error, event, state, **kwargs)

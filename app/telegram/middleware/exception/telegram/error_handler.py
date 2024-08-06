from aiogram.exceptions import TelegramAPIError
from app.telegram.middleware.exception.error_handler import ErrorHandler
from app.telegram.loader.base_loader import BaseLoader

class TelegramErrorHandler(ErrorHandler):
    def __init__(self, loader: BaseLoader):
        super().__init__(self.default_error_message)
        self.loader = loader
        self.register_handlers()

    def register_handlers(self):
        super().register_message_handler(TelegramAPIError, self.default_error_message)

    async def default_error_message(self, error: TelegramAPIError, state, **kwargs):
        return await self.loader.get_message_template(state, "telegram_error", "generic", **kwargs)

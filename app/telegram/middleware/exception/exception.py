import logging
import traceback
from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
from app.telegram.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.error_manager import ErrorManager

class ExceptionMiddleware(BaseMiddleware):
    def __init__(self, loader: BaseLoader):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.loader: BaseLoader = loader
        self.error_manager = ErrorManager(loader)
        self.error_manager.register_error_handlers()

    async def __call__(self, handler, event: Update, data: dict):
        state: FSMContext = data.get('state')
        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.error(traceback.format_exc())
            await self.error_manager.handle_error(e, event, state)

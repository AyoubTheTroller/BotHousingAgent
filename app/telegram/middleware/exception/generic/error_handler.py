import logging
from app.telegram.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.error_handler import ErrorHandler

class GenericErrorHandler(ErrorHandler):
    def __init__(self, loader: BaseLoader):
        super().__init__(self.default_error_message)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.loader = loader
        self.register_handlers()

    def register_handlers(self):
        super().register_message_handler(ValueError, self.value_error_message)

    async def default_error_message(self, error: Exception, state, **kwargs):
        return await self.loader.get_message_template(state, "generic_error", "generic", **kwargs)
    
    async def value_error_message(self, error: ValueError, state, **kwargs):
        return await self.loader.get_message_template(state, "generic_error", "generic", **kwargs)

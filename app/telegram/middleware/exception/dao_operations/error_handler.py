from app.telegram.middleware.exception.error_handler import ErrorHandler
from app.telegram.loader.base_loader import BaseLoader
from app.telegram.middleware.exception.dao_operations.custom_exceptions import DaoError, UserUpdateError, UserDataNotFoundError

class DaoErrorHandler(ErrorHandler):
    def __init__(self, loader: BaseLoader):
        super().__init__(self.default_error_message)
        self.loader = loader
        self.register_handlers()

    def register_handlers(self):
        super().register_message_handler(UserUpdateError, self.user_update_error_message)
        super().register_message_handler(UserDataNotFoundError, self.user_data_not_found_error_message)

    async def default_error_message(self, error: DaoError, state, **kwargs):
        return await self.loader.get_message_template(state, "dao_error", error.template_key, **kwargs)

    async def user_update_error_message(self, error: UserUpdateError, state, **kwargs):
        return await self.loader.get_message_template(state, "dao_error", "user_update_error", error.template_key, **kwargs)
    
    async def user_data_not_found_error_message(self, error: UserDataNotFoundError, state, **kwargs):
        return await self.loader.get_message_template(state, "dao_error", "user_data_not_found_error", error.template_key, **kwargs)

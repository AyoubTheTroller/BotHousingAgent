from aiohttp.client_exceptions import ClientResponseError
from aiogram.types import Update
from app.telegram.middleware.exception.generic.error_handler import GenericErrorHandler
from app.telegram.loader.base_loader import BaseLoader

class HttpClientErrorHandler:
    def __init__(self, loader: BaseLoader, generic_handler: GenericErrorHandler):
        self.loader = loader
        self.generic_handler = generic_handler
        self.logger = self.generic_handler.logger

        # Register specific error handler for HTTP client errors
        self.generic_handler.register_error_handler(ClientResponseError, self.handle_client_response_error)

    async def handle_client_response_error(self, error: ClientResponseError, event: Update, state):
        message = f"HTTP Client Response error: {error.status}, {error.message}, URL: {error.request_info.url}"
        keys = ["http_client_error","client_response","telegram"]
        self.logger.error(message)
        if error.status == 404:
            await event.message.answer(await self.loader.get_message_template(state,*keys,"not_found_error"))
        elif error.status == 500:
            await event.message.answer(await self.loader.get_message_template(state,*keys,"server_error"))
        else:
            await event.message.answer(await self.loader.get_message_template(state,*keys,"http_error"))

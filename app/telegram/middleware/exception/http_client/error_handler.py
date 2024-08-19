from aiohttp.client_exceptions import ClientError, ClientResponseError
from app.telegram.middleware.exception.error_handler import ErrorHandler
from app.telegram.loader.base_loader import BaseLoader

class HttpClientErrorHandler(ErrorHandler):
    def __init__(self, loader: BaseLoader):
        super().__init__(self.default_error_message)
        self.loader = loader
        self.register_handlers()

    def register_handlers(self):
        super().register_message_handler(ClientResponseError, self.client_response_error_message)

    async def default_error_message(self, error: ClientError, state, **kwargs):
        return await self.loader.get_message_template(state, "http_client_error", "generic", **kwargs)

    async def client_response_error_message(self, error: ClientResponseError, state, **kwargs):
        keys = ["http_client_error","client_response","telegram"]
        return await self.loader.get_message_template(state,*keys,str(error.status), **kwargs)
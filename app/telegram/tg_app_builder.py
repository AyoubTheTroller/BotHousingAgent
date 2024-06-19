from telegram.ext import ApplicationBuilder

class TelegramApplicationBuilder:
    """Needed to set configuration and returns the application builded"""

    def __init__(self, token):
        self._token = token

    def build(self):
        """Builds and returns the Telegram application instance."""
        return ApplicationBuilder().token(self._token).build()

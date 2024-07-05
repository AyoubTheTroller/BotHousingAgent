from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

class BotBuilder:
    """Needed to set configuration and returns the bot"""

    def __init__(self, token):
        self._token = token

    def build(self):
        """Builds and returns the Bot instance."""
        return Bot(token=self._token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

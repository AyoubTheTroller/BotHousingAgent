import asyncio
import logging
from aiogram import Bot
from app.telegram.bot_dispatcher import BotDispatcher

class TelegramApplication:

    def __init__(self, bot_dispatcher: BotDispatcher):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.logger.info("Telegram Application Started!")
        self.application : None
        self.bot_dispatcher = bot_dispatcher
        self.dispatcher = bot_dispatcher.dispatcher

    async def start_polling(self):
        await self.dispatcher.start_polling(self.application)

    def run_app(self, application: Bot):
        self.application = application
        self.dispatcher.shutdown.register(self.on_shutdown)
        try:
            asyncio.run(self.start_polling())
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt detected. Shutting down...")
            asyncio.run(self.on_shutdown())
        finally:
            self.logger.info("Application has been terminated.")

    async def on_shutdown(self):
        await self.dispatcher.storage.close()
        await self.application.session.close()

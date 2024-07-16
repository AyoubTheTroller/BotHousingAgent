import asyncio
import logging
from aiogram import Bot
from app.telegram.bot_controller import BotController

class TelegramApplication:

    def __init__(self, bot_controller: BotController):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.bot: Bot = bot_controller.bot
        self.bot_controller = bot_controller
        self.dispatcher = bot_controller.dispatcher

    async def start_polling(self):
        self.logger.info("Telegram Application Started!")
        await self.dispatcher.start_polling(self.bot)

    def run_app(self):
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
        await self.bot.session.close()

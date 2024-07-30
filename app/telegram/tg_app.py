from asyncio import AbstractEventLoop
import logging
from aiogram import Bot
from app.telegram.bot_controller import BotController

class TelegramApplication:
    def __init__(self, bot_controller: BotController, event_loop: AbstractEventLoop):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.bot: Bot = bot_controller.bot
        self.bot_controller = bot_controller
        self.dispatcher = bot_controller.dispatcher
        self.event_loop = event_loop

    async def start_polling(self):
        self.logger.info("Telegram Application Started!")
        await self.dispatcher.start_polling(self.bot)

    def run_app(self):
        # Register shutdown handler
        self.dispatcher.shutdown.register(self.on_shutdown)
        try:
            self.event_loop.create_task(self.start_polling())
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt detected. Shutting down...")
            self.event_loop.run_until_complete(self.on_shutdown())
        finally:
            self.logger.info("Application has been terminated.")

    async def on_shutdown(self):
        await self.dispatcher.storage.close()
        await self.bot.session.close()

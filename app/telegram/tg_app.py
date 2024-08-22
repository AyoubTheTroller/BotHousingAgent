import asyncio
from asyncio import AbstractEventLoop
import logging
from aiogram import Bot
from app.telegram.bot_controller import BotController

class TelegramApplication:
    def __init__(self, bot_controller: BotController, event_loop: AbstractEventLoop):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.bot: Bot = bot_controller.bot
        self.bot_controller = bot_controller
        self.dispatcher = bot_controller.dispatcher
        self.event_loop = event_loop

    async def start_polling(self):
        self.logger.info("Telegram Application Started!")
        await self.dispatcher.start_polling(self.bot)

    def run_app(self):
        asyncio.set_event_loop(self.event_loop)
        try:
            self.event_loop.run_until_complete(self.start_polling())
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt detected. Shutting down...")
        except Exception as e:
            self.logger.exception("Unexpected error occurred: %s", e)
        finally:
            self.event_loop.run_until_complete(self.shutdown())
            self.event_loop.close()
            self.logger.info("Application has been terminated.")

    async def shutdown(self):
        await self.on_shutdown()
        self.event_loop.stop()
        self.logger.info("Event loop stopped.")

    async def on_shutdown(self):
        self.logger.info("Shutting down Telegram bot...")
        await self.dispatcher.storage.close()
        await self.bot.session.close()
        self.logger.info("Shutdown complete.")

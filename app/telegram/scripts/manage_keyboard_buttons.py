import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

class ManageButtons:
    def __init__(self, token):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.setup_handlers()
        self.dispatcher.include_router(self.router)
        self.dispatcher.shutdown.register(self.on_shutdown)

    async def start_polling(self):
        await self.dispatcher.start_polling(self.bot, skip_updates=True)

    async def on_shutdown(self):
        await self.dispatcher.storage.close()
        await self.bot.session.close()

    def setup_handlers(self):
        # Register handlers if needed
        self.router.message.register(self.handle_add_test, Command('add_test'))
        self.router.message.register(self.handle_remove_all, Command('remove_all'))

    async def handle_add_test(self, message: types.Message):
        """Handler to add one test button."""
        await self.add_test_button(message)

    async def handle_remove_all(self, message: types.Message):
        """Handler to remove all buttons."""
        await self.remove_all_buttons(message)

    async def add_test_button(self, message: types.Message):
        """Add one test button."""
        # Creating the keyboard with explicit `keyboard` argument
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Test Button")]
            ],
            resize_keyboard=True
        )
        await message.answer("Test button added:", reply_markup=markup)

    async def remove_all_buttons(self, message: types.Message):
        """Remove all buttons."""
        await message.answer("All buttons removed.", reply_markup=ReplyKeyboardRemove())

async def main():
    load_dotenv()  # Load environment variables from .env file
    bot_token = os.getenv('BOT_TOKEN')  # Read the BOT_TOKEN environment variable
    manage = ManageButtons(bot_token)
    await manage.start_polling()

# Usage
if __name__ == "__main__":
    asyncio.run(main())

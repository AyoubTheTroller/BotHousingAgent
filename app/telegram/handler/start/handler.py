from aiogram.types import Message
from app.telegram.handler.loader import Loader

class StartHandler:
    def __init__(self, loader: Loader):
        self.loader = loader

    async def start_command(self, message: Message):
        welcome = self.loader.get_message_template("welcome")
        instructions = self.loader.get_message_template("instructions")
        commands = self.loader.get_message_template("commands")
        await message.answer(f"{welcome}\n\n{instructions}\n\n{commands}")
        await self.load_keyboard_buttons(message)

    async def load_keyboard_buttons(self, message: Message):
        markup = self.loader.create_keyboard_buttons_markup(["Start","Help","Search House"])
        await message.answer(text="Buttons added",reply_markup=markup)

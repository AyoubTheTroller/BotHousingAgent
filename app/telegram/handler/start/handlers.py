from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from app.telegram.handler.loader.components_loader import ComponentsLoader

class StartHandler:
    def __init__(self, loader: ComponentsLoader):
        self.loader = loader

    async def start_command(self, message: Message):
        welcome = self.loader.get_message_template("welcome")
        instructions = self.loader.get_message_template("instructions")
        commands = self.loader.get_message_template("commands")
        await message.answer(f"{welcome}\n\n{instructions}\n\n{commands}")

    async def show_menu(self, message: Message):
        markup = self.loader.create_keyboard_buttons_markup(["Start","Help","Search House"])
        if message.reply_markup and isinstance(message.reply_markup, ReplyKeyboardMarkup):
            await message.edit_reply_markup(reply_markup=markup)
        else:
            await message.answer(self.loader.get_message_template("show_menu"), reply_markup=markup)

    async def hide_menu(self, message: Message) -> None:
        await message.answer(self.loader.get_message_template("hide_menu"), reply_markup=ReplyKeyboardRemove())

from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from app.telegram.handler.loader.components_loader import ComponentsLoader

class MenuHandler:
    def __init__(self, loader: ComponentsLoader):
        self.loader = loader

    async def show_menu(self, message: Message):
        buttons = [self.loader.get_keyboard_button_template("start"),
                   self.loader.get_keyboard_button_template("help"),
                   self.loader.get_keyboard_button_template("search_house")]
        markup = self.loader.create_keyboard_buttons_markup(buttons)
        await message.answer(self.loader.get_message_template("show_menu"), reply_markup=markup)

    async def hide_menu(self, message: Message) -> None:
        await message.answer(self.loader.get_message_template("hide_menu"), reply_markup=ReplyKeyboardRemove())

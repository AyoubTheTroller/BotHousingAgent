from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader

class MenuHandler:
    def __init__(self, loader: ComponentsLoader):
        self.loader = loader

    async def show_menu(self, message: Message, state: FSMContext):
        buttons = [await self.loader.get_keyboard_button_template("start", state),
                   await self.loader.get_keyboard_button_template("help", state),
                   await self.loader.get_keyboard_button_template("search_house", state)]
        markup = self.loader.create_keyboard_buttons_markup(buttons)
        await message.answer(self.loader.get_message_template("show_menu", state), reply_markup=markup)

    async def hide_menu(self, message: Message, state: FSMContext) -> None:
        await message.answer(self.loader.get_message_template("hide_menu", state), reply_markup=ReplyKeyboardRemove())

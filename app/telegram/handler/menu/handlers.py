from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader

class MenuHandler:
    def __init__(self, loader: ComponentsLoader):
        self.loader = loader

    async def show_menu(self, message: Message, state: FSMContext):
        buttons = [await self.loader.get_keyboard_button_template(state, "start"),
                   await self.loader.get_keyboard_button_template(state, "help"),
                   await self.loader.get_keyboard_button_template(state, "set_search_filters")]
        markup = self.loader.create_keyboard_buttons_markup(buttons)
        await message.answer(await self.loader.get_message_template(state, "show_menu"), reply_markup=markup)

    async def hide_menu(self, message: Message, state: FSMContext) -> None:
        await message.answer(await self.loader.get_message_template(state, "hide_menu"), reply_markup=ReplyKeyboardRemove())

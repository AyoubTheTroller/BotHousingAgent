from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from app.telegram.loader.base_loader import BaseLoader

class ComponentsLoader(BaseLoader):

    async def create_inline_keyboard_button_markup(self, button_text: str, callback_data) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from one button data.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data=callback_data)]]
        )
        return keyboard

    def create_inline_keyboard_buttons_markup_from_template(self, buttons: List) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=text)] for text in buttons]
        )
        return keyboard
    
    def create_inline_keyboard_buttons_with_callback(self, buttons: List) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data.
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for button in buttons:
            text, callback_data = self.split_button_data(button)
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

        return keyboard
    
    def split_button_data(self, button: str) -> Tuple[str,str]:
        """returns button data as tuple, one part is the text shown the other is the callback data """
        parts = button.split('.')
        if len(parts) == 2:
            return parts[0], parts[1]
        
    def create_inline_keyboard_buttons_markup(self, buttons: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data represented as tuples.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text, callback_data=callback)]
                for text, callback in buttons
            ]
        )
        return keyboard

    def create_keyboard_buttons_markup(self, buttons: List) -> ReplyKeyboardMarkup:
        """
        Creates a reply keyboard markup from a list of buttons
        """
        markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = button) for button in buttons]],
                                     resize_keyboard=True,
                                     one_time_keyboard=False)
        return markup

    async def append_button_to_markup(self, text, callback_data, keyboard_markup = None) -> InlineKeyboardMarkup:
        if keyboard_markup is None:
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
        return keyboard_markup

    async def add_skip_buttons(self, state: FSMContext, keyboard_markup = None) -> InlineKeyboardMarkup:
        skip_step = await super().get_keyboard_button_template(state, "skip_step")
        go_to_search = await super().get_keyboard_button_template(state, "go_to_search")
        if keyboard_markup is None:
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=skip_step, callback_data="skip_step")])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=go_to_search, callback_data="go_to_search")])
        return keyboard_markup
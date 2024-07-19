from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from app.service.template.telegram.template_service import TelegramTemplateService

class ComponentsLoader():
    def __init__(self,
                 template_service: TelegramTemplateService,
                 interaction_type: str,
                 handler_type: str):

        self.template_service = template_service
        self.interaction_type = interaction_type
        self.handler_type = handler_type

    def get_message_template(self, key, **kwargs):
        """Helper function to return the message from a template."""
        return self.template_service.render_template(self.interaction_type, self.handler_type, "message", key, **kwargs)

    def get_keyboard_button_template(self, key):
        """Helper function to return the array of keyboard templates"""
        return self.template_service.render_template(self.interaction_type, self.handler_type, "button", key)
    
    def create_inline_keyboard_button_markup(self, button_text: str, callback_data) -> InlineKeyboardMarkup:
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
    
    def append_button_to_markup(self, keyboard_markup: InlineKeyboardMarkup, text, callback_data) -> InlineKeyboardMarkup:
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
        return keyboard_markup
    
    def add_skip_buttons(self, keyboard_markup = None) -> InlineKeyboardMarkup:
        skip_step = self.get_keyboard_button_template("skip_step")
        go_to_search = self.get_keyboard_button_template("go_to_search")
        if keyboard_markup is None:
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=skip_step, callback_data="skip_step")])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=go_to_search, callback_data="go_to_search")])
        return keyboard_markup

from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.service.mongodb.mongo_service import MongoService
from app.service.template.template_service import TemplateService

class Loader():
    def __init__(self,
                 mongo_service: MongoService,
                 template_service: TemplateService,
                 interaction_type: str,
                 handler_type: str):
        
        self.mongo_service = mongo_service
        self.template_service = template_service
        self.interaction_type = interaction_type
        self.handler_type = handler_type

    def get_message_template(self, key, **kwargs):
        """Helper function to return the message from a template."""
        return self.template_service.render_telegram_template(self.interaction_type, self.handler_type, "message", key, **kwargs)

    def get_keyboard_button_template(self, key):
        """Helper function to return the array of keyboard templates"""
        return self.template_service.render_telegram_template(self.interaction_type, self.handler_type, "button", key)
    
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

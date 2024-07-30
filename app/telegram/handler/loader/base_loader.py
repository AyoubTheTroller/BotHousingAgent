from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.service.template.telegram.template_service import TelegramTemplateService

class BaseLoader():
    def __init__(self,
                 template_service: TelegramTemplateService,
                 interaction_type: str,
                 handler_type: str):

        self.template_service = template_service
        self.interaction_type = interaction_type
        self.handler_type = handler_type

    async def get_old_message_template(self, key, state: FSMContext, **kwargs):
        """Helper function to return the message from a template."""
        user_data = await state.get_data()
        language = user_data.get('language')
        return await self.template_service.render_template(self.interaction_type, self.handler_type, "message", key, language, **kwargs)
    
    async def get_message_template(self, state: FSMContext, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        user_data = await state.get_data()
        language = user_data.get('language')
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)

    async def get_keyboard_button_template(self, state: FSMContext, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        user_data = await state.get_data()
        language = user_data.get('language')
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)

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

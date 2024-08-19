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

    async def get_language(self, state: FSMContext):
        if state:
            user_data = await state.get_data()
            return user_data.get('language')
        else:
            raise ValueError("Either state or language must be provided")

    def get_base_message_template(self, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        return self.template_service.render_base_template(self.interaction_type, self.handler_type, "message", *keys, **kwargs)
    
    def get_base_button_template(self, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        return self.template_service.render_base_template(self.interaction_type, self.handler_type, "button", *keys, **kwargs)

    async def get_message_template(self, state: FSMContext, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        language = await self.get_language(state)
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)
    
    async def get_keyboard_button_template(self, state: FSMContext, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        language = await self.get_language(state)
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)

    async def get_message_template_by_lang(self, language:str, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)
    
    async def get_keyboard_button_template_by_lang(self, language:str, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)
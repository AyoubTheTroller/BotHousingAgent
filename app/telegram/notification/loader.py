from app.service.template.telegram.template_service import TelegramTemplateService

class NotificationLoader():
    def __init__(self,
                 template_service: TelegramTemplateService,
                 interaction_type: str,
                 handler_type: str):

        self.template_service = template_service
        self.interaction_type = interaction_type
        self.handler_type = handler_type

    async def get_message_template(self, language, *keys, **kwargs):
        """Helper function to return the message from a template."""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)

    async def get_keyboard_button_template(self, language, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)


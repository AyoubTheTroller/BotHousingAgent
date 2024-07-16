from app.service.template.telegram.template_service import TelegramTemplateService

class BaseLoader():
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

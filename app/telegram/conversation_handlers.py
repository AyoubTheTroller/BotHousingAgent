from typing import List
from app.telegram.handler.prepare_url import PrepareUrl

class ConversationHandlers:

    def __init__(self, mongo_service, template_service):
        self.mongo_service = mongo_service
        self.template_service = template_service

    def get_handlers(self) -> List:
        """Returns a list of CommandHandler instances."""
        return [
            PrepareUrl(self.mongo_service,self.template_service).get_handler(),
            #other Handlers.
        ]

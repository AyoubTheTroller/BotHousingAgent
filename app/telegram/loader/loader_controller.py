import importlib
from app.service.template.telegram.template_service import TelegramTemplateService

loaders_module = {
    "BaseLoader": "app.telegram.loader.base_loader",
    "ComponentsLoader":"app.telegram.loader.components_loader",
    "SearchLoader":"app.telegram.loader.search_loader",
    "ConversationLoader":"app.telegram.loader.conversation_loader"
}

class LoaderController():
    def __init__(self, template_service: TelegramTemplateService):
        self._template_service = template_service
        self.loaders = {}
        self.create_loaders()

    def create_loaders(self):
        for interaction_type, values in self._template_service.telegram_templates.templates.items():
            self.loaders[interaction_type] = {}
            for handler_type, value in values.items():
                loader_type = value.get("type",{})
                self.loaders[interaction_type][handler_type] = self.instantiate_loader(loader_type, interaction_type, handler_type)
    
    def instantiate_loader(self, loader_type, interaction_type, handler_type):
        module_path=f"{loaders_module[loader_type]}"
        module = importlib.import_module(module_path)
        class_ = getattr(module, loader_type)
        return class_(self._template_service,interaction_type,handler_type)
    
    def get_loader(self, interaction_type: str, handler_type: str):
        return self.loaders.get(interaction_type).get(handler_type)

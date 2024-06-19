from dependency_injector import containers, providers

class TemplateContainer(containers.DeclarativeContainer):
    
    config = providers.Configuration()

from dependency_injector import containers, providers
from app.service.mongodb.mongo_service import MongoService
from app.service.template.template_service import TemplateService

class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mongo_client = providers.Dependency()

    templates = providers.DependenciesContainer()

    mongo_service = providers.Factory(
        MongoService,
        mongo_client,
    )

    template_service = providers.Factory(
        TemplateService,
        telegram_templates=templates.telegram_templates
    )

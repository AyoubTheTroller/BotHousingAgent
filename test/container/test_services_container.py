from dependency_injector import containers, providers
from app.container.core_container import CoreContainer
from app.container.db_container import DbContainer
from app.container.service_container import ServiceContainer

class ServicesTestContainer(containers.DeclarativeContainer):
    core = providers.Container(
        CoreContainer
    )

    db = providers.Container(
        DbContainer,
        config=core.app_config
    )

    services = providers.Container(
        ServiceContainer,
        config=core.app_config,
        mongo_client=db.mongo_client
    )

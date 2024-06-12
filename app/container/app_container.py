from dependency_injector import containers, providers
from app.container.db_container import DbContainer

class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    mongodb = providers.Container(
        DbContainer,
        config=config,
    )

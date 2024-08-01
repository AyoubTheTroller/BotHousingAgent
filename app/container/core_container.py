import logging.config
import asyncio
from dependency_injector import containers, providers
from app.config.config_loader import ConfigLoader

class CoreContainer(containers.DeclarativeContainer):

    config_loader = ConfigLoader("global-env.json")

    global_config = config_loader.load_global_config_provider()

    app_config = config_loader.load_app_config_provider()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=app_config.core.logging,
    )
    event_loop = providers.Singleton(asyncio.new_event_loop)

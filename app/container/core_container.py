import logging.config
import asyncio
from dependency_injector import containers, providers

class CoreContainer(containers.DeclarativeContainer):

    global_env = providers.Configuration("global-env.json")

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
    event_loop = providers.Singleton(asyncio.new_event_loop)

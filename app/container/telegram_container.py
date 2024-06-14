from dependency_injector import containers, providers
from app.telegram.tg_app import TelegramApplication

class TelegramContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    telegram_application = providers.Singleton(TelegramApplication, config.telegram.token)

from dependency_injector.wiring import Provide, inject
from app.config.config_loader import ConfigLoader
from app.container.app_container import ApplicationContainer
from app.telegram.tg_app import TelegramApplication

class SpawnApplicationContext:
    def __init__(self):
        self.config = ConfigLoader("global-env.json")
        self._setup_containers()

    def _setup_containers(self):
        container = ApplicationContainer(config=self.config.get_config_dict())
        container.wire(modules=[__name__])
        container.core.init_resources()
        self.try_injection()

    @inject
    def try_injection(self, tg_app: TelegramApplication= Provide[ApplicationContainer.tg_app.telegram_application]) -> None:
        pass

from dependency_injector.wiring import Provide, inject
from app.container.app_container import ApplicationContainer
from app.telegram.tg_app import TelegramApplication
from app.telegram.tg_app_builder import TelegramApplicationBuilder

class SpawnApplicationContext:
    def __init__(self):
        self._setup_containers()

    def _setup_containers(self):
        container = ApplicationContainer()
        container.wire(modules=[__name__])
        container.core.init_resources()
        container.mongodb.init_resources()
        container.telegram.init_resources()
        self.start_application()

    @inject
    def start_application(self, builder: TelegramApplicationBuilder = Provide[ApplicationContainer.telegram.telegram_application_builder],
                            tg_app: TelegramApplication = Provide[ApplicationContainer.telegram.telegram_application]) -> None:
        tg_app.run_app(builder.build())

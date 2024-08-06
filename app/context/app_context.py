from dependency_injector.wiring import Provide, inject
from app.container.app_container import ApplicationContainer
from app.telegram.tg_app import TelegramApplication

class SpawnApplicationContext:

    def __init__(self):
        self._setup_containers()

    def _setup_containers(self):
        container = ApplicationContainer()
        container.wire(modules=[
            'app.context.app_context',
            'app.service.search.search_service',
        ])
        container.core.init_resources()
        self.spawn()
    
    @inject
    def spawn(self, tg_app: TelegramApplication = Provide[ApplicationContainer.telegram.telegram_application]) -> None:
        tg_app.run_app()

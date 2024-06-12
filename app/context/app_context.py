from app.config.config_loader import ConfigLoader
from app.container.app_container import ApplicationContainer

class ApplicationContext:
    def __init__(self):
        self.config = ConfigLoader("global-env.json")
        self._setup_containers()

    def _setup_containers(self):
        container = ApplicationContainer()
        container.config.from_dict(self.config.get_config_dict())
        print(container.config())
        container.mongodb.init_resources()
        #container.wire(modules=[__name__])

    def run_bot(self):
        pass

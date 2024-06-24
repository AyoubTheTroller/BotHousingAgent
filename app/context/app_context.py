from dependency_injector.wiring import Provide, inject
from app.container.app_container import ApplicationContainer
from app.telegram.tg_app import TelegramApplication
from app.telegram.tg_app_builder import TelegramApplicationBuilder
from app.template.telegram.telegram_templates import TelegramTemplates

class SpawnApplicationContext:
    def __init__(self):
        self._setup_containers()

    def _setup_containers(self):
        container = ApplicationContainer()
        container.wire(modules=[__name__])
        container.core.init_resources()
        container.mongodb_package.init_resources()
        container.tg_package.init_resources()
        self.try_template()

    @inject
    def try_template(self, telegram_templates: TelegramTemplates = Provide[ApplicationContainer.templates_package.telegram_templates]) -> None:
        template = telegram_templates.get_template("conversation","get_search_param")
        print(template)

    @inject
    def try_injection(self, builder: TelegramApplicationBuilder = Provide[ApplicationContainer.tg_package.telegram_application_builder],
                            tg_app: TelegramApplication = Provide[ApplicationContainer.tg_package.telegram_application]) -> None:
        tg_app.run_app(builder.build())

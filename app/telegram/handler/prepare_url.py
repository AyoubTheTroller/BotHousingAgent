from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.service.mongodb.mongo_service import MongoService
from app.service.template.template_service import TemplateService

class PrepareUrl:
    
    def __init__(self, router: Router, mongo_service: MongoService, template_service: TemplateService):
        self.router = router
        self.mongo_service = mongo_service
        self.template_service = template_service
        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.prepare_url, Command(commands=["prepare_url"]))
        self.router.message.register(self.get_city,Form.get_city)

    async def prepare_url(self, message: Message, state: FSMContext):
        """Starts the conversation to collect URL parameters."""
        await self._reply_with_message_template(message, "start")
        await self._reply_with_message_template(message, "get_city")
        await state.set_state(Form.get_city)

    async def get_city(self, message: Message, state: FSMContext) -> int:
        """Gets the city from the user."""
        await state.update_data(city=message.text)
        await self._reply_with_message_template(message, "get_max_price")

        #await state.set_state(self.MAX_PRICE)

    async def _reply_with_message_template(self, message: Message, template_key: str):
        """Helper function to send a message using a template."""
        message_text = self.template_service.render_telegram_template("conversation", "get_search_param", "message", template_key)
        await message.answer(message_text)


class Form(StatesGroup):
    name = State()
    get_city = State()
    get_max_price = State()

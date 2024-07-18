from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.service.scraping.scraping_service import ScrapingService
from app.scraping.model.query_params import QueryParams

class Form(StatesGroup):
    city_name = State()
    max_price = State()
    appartment_type = State()
    furnished = State()
    confirmation = State()

class SearchParamsHandlers():

    def __init__(self, loader: ComponentsLoader, scraping_service: ScrapingService):
        self.loader = loader
        self.scraping_service = scraping_service

    async def search_house(self, message: Message):
        await message.answer(
            self.loader.get_message_template("start"),
            reply_markup=self.loader.create_inline_keyboard_button_markup("Go to form", "start")
        )

    async def handle_start(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.city_name)
        await self.city_name(callback_query.message)

    async def city_name(self, message: Message):
        await message.answer(self.loader.get_message_template("get_city"))

    async def handle_city_name(self, message: Message, state: FSMContext):
        city_name = message.text
        await state.update_data(city_name=city_name)
        await state.set_state(Form.max_price)
        await self.max_price(message)

    async def max_price(self, message: Message):
        await message.answer(self.loader.get_message_template("get_max_price"))

    async def handle_max_price(self, message: Message, state: FSMContext):
        max_price = message.text
        if not max_price.isdigit() or int(max_price) <= 0:
            await message.answer(self.loader.get_message_template("invalid_price"))
            return
        await state.update_data(max_price=max_price)
        await state.set_state(Form.appartment_type)
        await self.appartment_type(message)

    async def appartment_type(self, message: Message):
        appartment_types = self.loader.get_keyboard_button_template("appartment_types")
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(appartment_types)
        await message.answer(self.loader.get_message_template("get_appartment_type"),reply_markup=keyboard_markup)

    async def handle_appartment_type(self, callback_query: CallbackQuery, state: FSMContext):
        appartment_type = callback_query.data
        await state.update_data(appartment_type=appartment_type)
        await state.set_state(Form.furnished)
        await self.furnished(callback_query.message)

    async def furnished(self, message: Message):
        furnished = self.loader.get_keyboard_button_template("furnished")
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(furnished)
        await message.answer(self.loader.get_message_template("get_furnished"), reply_markup=keyboard_markup)

    async def handle_furnished(self, callback_query: CallbackQuery, state: FSMContext):
        furnished = callback_query.data
        await state.update_data(furnished=furnished)
        await state.set_state(Form.confirmation)
        await self.confirmation(callback_query.message, state)

    async def confirmation(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        confirmation_text = self.loader.get_message_template("ask_confirmation",
                                                             city_name=user_data['city_name'],
                                                             max_price=user_data['max_price'],
                                                             appartment_type=user_data['appartment_type'],
                                                             furnished=user_data['furnished'])
        buttons = [(self.loader.get_message_template("yes"),"yes"),
                   (self.loader.get_message_template("no"),"no")]
        keyboard = self.loader.create_inline_keyboard_buttons_markup(buttons)
        await message.answer(confirmation_text, reply_markup=keyboard)

    async def handle_confirmation(self, callback_query: CallbackQuery, state: FSMContext):
        confirmation = callback_query.data
        if confirmation == "yes":
            user_data = await state.get_data()
            processed_user_data = self.preprocess_input_data(user_data)
            query_params = QueryParams(**processed_user_data)
            url_builder = self.scraping_service.scraping_controller.website_scraping_register.get_url_builder("immobiliare")
            url = url_builder.build_url(query_params)
            await callback_query.message.answer(url)
            await state.clear()
        elif confirmation == "no":
            await callback_query.message.answer("Restarting the process. Please start over.")
            await state.finish()

    def preprocess_input_data(self,data: dict) -> dict:
        # Map 'si'/'no' to True/False
        boolean_fields = ['furnished', 'balcony_or_terrace', 'balcony', 'terrace', 'piscina', 'cellar']
        for field in boolean_fields:
            if field in data:
                if data[field].lower() in ['si', 'yes', 'true']:
                    data[field] = True
                elif data[field].lower() in ['no', 'false']:
                    data[field] = False
                else:
                    data[field] = None  # or raise an error if you want strict validation
        return data

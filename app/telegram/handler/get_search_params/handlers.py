from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.service.scraping.scraping_service import ScrapingService
from app.scraping.model.query_params import QueryParams

class Form(StatesGroup):
    city_name = State()
    max_price = State()
    min_rooms = State()
    max_rooms = State()
    n_bathrooms = State()
    appartment_type = State()
    furnished = State()
    balcony = State()
    terrace = State()
    pool = State()
    cellar = State()
    confirmation = State()
    prepare_url = State()
    scraping = State()

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
        keyboard_markup = self.loader.add_skip_buttons()
        await message.answer(self.loader.get_message_template("get_max_price"), reply_markup=keyboard_markup)

    async def handle_max_price(self, message: Message, state: FSMContext):
        max_price = message.text
        if not max_price.isdigit() or int(max_price) <= 0:
            await message.answer(self.loader.get_message_template("invalid_price"))
            return
        await state.update_data(max_price=max_price)
        await state.set_state(Form.min_rooms)
        await self.min_rooms(message)
    
    async def min_rooms(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4","5"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_min_rooms"), reply_markup=keyboard_markup)

    async def handle_min_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        min_rooms = callback_query.data
        await state.update_data(min_rooms=min_rooms)
        await state.set_state(Form.max_rooms)
        await self.max_rooms(callback_query.message)

    async def max_rooms(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4","5"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_max_rooms"), reply_markup=keyboard_markup)

    async def handle_max_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        max_rooms = callback_query.data
        await state.update_data(max_rooms=max_rooms)
        await state.set_state(Form.n_bathrooms)
        await self.n_bathrooms(callback_query.message)

    async def n_bathrooms(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_n_bathrooms"), reply_markup=keyboard_markup)

    async def handle_n_bathrooms(self, callback_query: CallbackQuery, state: FSMContext):
        bathrooms = callback_query.data
        await state.update_data(bathrooms=bathrooms)
        await state.set_state(Form.furnished)
        await self.furnished(callback_query.message)

    async def furnished(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_furnished"), reply_markup=keyboard_markup)

    async def handle_furnished(self, callback_query: CallbackQuery, state: FSMContext):
        furnished = callback_query.data
        await state.update_data(furnished=furnished)
        await state.set_state(Form.balcony)
        await self.balcony(callback_query.message)

    async def balcony(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_balcony"), reply_markup=keyboard_markup)

    async def handle_balcony(self, callback_query: CallbackQuery, state: FSMContext):
        balcony = callback_query.data
        await state.update_data(balcony=balcony)
        await state.set_state(Form.terrace)
        await self.terrace(callback_query.message)

    async def terrace(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_terrace"), reply_markup=keyboard_markup)

    async def handle_terrace(self, callback_query: CallbackQuery, state: FSMContext):
        terrace = callback_query.data
        await state.update_data(terrace=terrace)
        await state.set_state(Form.pool)
        await self.pool(callback_query.message)

    async def pool(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_pool"), reply_markup=keyboard_markup)

    async def handle_pool(self, callback_query: CallbackQuery, state: FSMContext):
        pool = callback_query.data
        await state.update_data(pool=pool)
        await state.set_state(Form.cellar)
        await self.cellar(callback_query.message)

    async def cellar(self, message: Message):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = self.loader.add_skip_buttons(keyboard_markup)
        await message.answer(self.loader.get_message_template("get_cellar"), reply_markup=keyboard_markup)

    async def handle_cellar(self, callback_query: CallbackQuery, state: FSMContext):
        cellar = callback_query.data
        await state.update_data(cellar=cellar)
        await state.set_state(Form.prepare_url)
        await self.prepare_url(callback_query, state)

    def preprocess_input_data(self,data: dict) -> dict:
        boolean_fields = ['furnished', 'balcony_or_terrace', 'balcony', 'terrace', 'piscina', 'cellar', 'pool']
        for field in boolean_fields:
            if field in data:
                if data[field].lower() in ['si', 'yes', 'true']:
                    data[field] = True
                elif data[field].lower() in ['no', 'false']:
                    data[field] = False
                else:
                    data[field] = None  # or raise an error if you want strict validation
        return data
    
    async def handle_skip_step(self, callback_query: CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state == Form.max_price:
            await state.set_state(Form.min_rooms)
            await self.min_rooms(callback_query.message)
        elif current_state == Form.min_rooms:
            await state.set_state(Form.max_rooms)
            await self.max_rooms(callback_query.message)
        elif current_state == Form.max_rooms:
            await state.set_state(Form.n_bathrooms)
            await self.n_bathrooms(callback_query.message)
        elif current_state == Form.n_bathrooms:
            await state.set_state(Form.furnished)
            await self.furnished(callback_query.message)
        elif current_state == Form.furnished:
            await state.set_state(Form.balcony)
            await self.balcony(callback_query.message)
        elif current_state == Form.balcony:
            await state.set_state(Form.terrace)
            await self.terrace(callback_query.message)
        elif current_state == Form.terrace:
            await state.set_state(Form.pool)
            await self.pool(callback_query.message)
        elif current_state == Form.pool:
            await state.set_state(Form.cellar)
            await self.cellar(callback_query.message)
        elif current_state == Form.cellar:
            await state.set_state(Form.prepare_url)
            await self.prepare_url(callback_query, state)

    async def handle_go_to_search(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.prepare_url)
        await self.prepare_url(callback_query, state)

    async def prepare_url(self, callback_query: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        processed_user_data = self.preprocess_input_data(user_data)
        query_params = QueryParams(**processed_user_data)
        url_builder = self.scraping_service.scraping_controller.website_scraping_register.get_url_builder("immobiliare")
        url = url_builder.build_url(query_params)
        await callback_query.message.answer(url)
        await state.clear()

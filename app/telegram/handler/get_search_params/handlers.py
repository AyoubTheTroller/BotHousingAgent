import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader
from app.service.scraping.scraping_service import ScrapingService
from app.scraping.model.search_params import SearchParams

class Form(StatesGroup):
    search_type = State()
    location = State()
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
    end = State()

class SearchParamsHandlers():

    def __init__(self, loader: ComponentsLoader, scraping_service: ScrapingService):
        self.loader = loader
        self.scraping_service = scraping_service

    async def search_house(self, message: Message, state: FSMContext):
        await message.answer(
            await self.loader.get_message_template(state, "start"),
            reply_markup=self.loader.create_inline_keyboard_button_markup(
                await self.loader.get_keyboard_button_template(state, "go_to_form"), "start"))

    async def handle_start(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.search_type)
        await self.search_type(callback_query.message, state)

    async def search_type(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state, "search_type"))
        await message.answer(await self.loader.get_message_template(state, "search_type"), reply_markup=keyboard_markup)

    async def handle_search_type(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(search_type=callback_query.data)
        await state.set_state(Form.location)
        await self.location(callback_query.message, state)

    async def location(self, message: Message, state: FSMContext):
        await message.answer(await self.loader.get_message_template(state, "get_city"))

    async def handle_location(self, message: Message, state: FSMContext):
        await state.update_data(location=message.text)
        await state.set_state(Form.max_price)
        await self.max_price(message, state)

    async def max_price(self, message: Message, state: FSMContext):
        keyboard_markup = await self.loader.add_skip_buttons(state)
        await message.answer(await self.loader.get_message_template(state, "get_max_price"), reply_markup=keyboard_markup)

    async def handle_max_price(self, message: Message, state: FSMContext):
        max_price = message.text
        if not max_price.isdigit() or int(max_price) <= 0:
            await message.answer(await self.loader.get_message_template(state, "invalid_price"))
            return
        await state.update_data(max_price=max_price)
        await state.set_state(Form.min_rooms)
        await self.min_rooms(message, state)
    
    async def min_rooms(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4","5"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_min_rooms"), reply_markup=keyboard_markup)

    async def handle_min_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(min_rooms=callback_query.data)
        await state.set_state(Form.max_rooms)
        await self.max_rooms(callback_query.message, state)

    async def max_rooms(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4","5"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_max_rooms"), reply_markup=keyboard_markup)

    async def handle_max_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(max_rooms=callback_query.data)
        await state.set_state(Form.n_bathrooms)
        await self.n_bathrooms(callback_query.message, state)

    async def n_bathrooms(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_n_bathrooms"), reply_markup=keyboard_markup)

    async def handle_n_bathrooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(bathrooms=callback_query.data)
        await state.set_state(Form.furnished)
        await self.furnished(callback_query.message, state)

    async def furnished(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_furnished"), reply_markup=keyboard_markup)

    async def handle_furnished(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(furnished=callback_query.data)
        await state.set_state(Form.balcony)
        await self.balcony(callback_query.message, state)

    async def balcony(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_balcony"), reply_markup=keyboard_markup)

    async def handle_balcony(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(balcony=callback_query.data)
        await state.set_state(Form.terrace)
        await self.terrace(callback_query.message, state)

    async def terrace(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_terrace"), reply_markup=keyboard_markup)

    async def handle_terrace(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(terrace=callback_query.data)
        await state.set_state(Form.pool)
        await self.pool(callback_query.message, state)

    async def pool(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_pool"), reply_markup=keyboard_markup)

    async def handle_pool(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(pool=callback_query.data)
        await state.set_state(Form.cellar)
        await self.cellar(callback_query.message, state)

    async def cellar(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["yes","no"])
        keyboard_markup = await self.loader.add_skip_buttons(state, keyboard_markup)
        await message.answer(await self.loader.get_message_template(state, "get_cellar"), reply_markup=keyboard_markup)

    async def handle_cellar(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(cellar=callback_query.data)
        await state.set_state(Form.prepare_url)
        await self.prepare_url(callback_query, state)
    
    async def handle_skip_step(self, callback_query: CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state == Form.max_price:
            await state.set_state(Form.min_rooms)
            await self.min_rooms(callback_query.message, state)
        elif current_state == Form.min_rooms:
            await state.set_state(Form.max_rooms)
            await self.max_rooms(callback_query.message, state)
        elif current_state == Form.max_rooms:
            await state.set_state(Form.n_bathrooms)
            await self.n_bathrooms(callback_query.message, state)
        elif current_state == Form.n_bathrooms:
            await state.set_state(Form.furnished)
            await self.furnished(callback_query.message, state)
        elif current_state == Form.furnished:
            await state.set_state(Form.balcony)
            await self.balcony(callback_query.message, state)
        elif current_state == Form.balcony:
            await state.set_state(Form.terrace)
            await self.terrace(callback_query.message, state)
        elif current_state == Form.terrace:
            await state.set_state(Form.pool)
            await self.pool(callback_query.message, state)
        elif current_state == Form.pool:
            await state.set_state(Form.cellar)
            await self.cellar(callback_query.message, state)
        elif current_state == Form.cellar:
            await state.set_state(Form.prepare_url)
            await self.prepare_url(callback_query, state)

    async def handle_go_to_search(self, callback_query: CallbackQuery, state: FSMContext):
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

    async def prepare_url(self, callback_query: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        processed_user_data = self.preprocess_input_data(user_data)
        language = user_data.get('language')
        search_params = SearchParams(**processed_user_data)
        url = await self.scraping_service.build_url(search_params)
        await callback_query.message.answer(url)
        await callback_query.message.answer(await self.loader.get_message_template(state, "searching"))
        await self.post_house_listings(url, language, callback_query, state)
    
    async def post_house_listings(self, url, language, callback_query: CallbackQuery, state: FSMContext):
        listings = await self.scraping_service.scrape_listings(url)
        if not listings:
            await callback_query.message.answer(
                text=await self.loader.get_message_template_with_lang(language, "no_listings_found"), parse_mode="HTML")
        else:
            for listing in listings:
                media_group = await self.loader.load_listing_photos(listing)
                keyboard = await self.loader.load_listing_with_keyboard(listing, language)
                message_text = await self.loader.load_listing_message(listing, language)
                if media_group is not None:
                    await callback_query.message.answer_media_group(media_group)
                await callback_query.message.answer(message_text, reply_markup=keyboard, parse_mode="HTML")
                await asyncio.sleep(3) # to handle flood control
            await callback_query.message.answer(await self.loader.get_message_template_with_lang(language, "search_completed"))
        await state.set_state(Form.end)

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram.loader.components_loader import ComponentsLoader
from app.scraping.model.search_params import SearchParams
from app.service.search.search_service import SearchService

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
    prepare_for_search = State()
    searching = State()
    end = State()

PREV_STEP_TRANSITIONS = {
    Form.max_price: (Form.location, "location"),
    Form.min_rooms: (Form.max_price, "max_price"),
    Form.max_rooms: (Form.min_rooms, "min_rooms"),
    Form.n_bathrooms: (Form.max_rooms, "max_rooms"),
    Form.furnished: (Form.n_bathrooms, "n_bathrooms"),
    Form.balcony: (Form.furnished, "furnished"),
    Form.terrace: (Form.balcony, "balcony"),
    Form.pool: (Form.terrace, "terrace"),
    Form.cellar: (Form.pool, "pool"),
}

SKIP_STEP_TRANSITIONS = {
    Form.max_price: (Form.min_rooms, "min_rooms"),
    Form.min_rooms: (Form.max_rooms, "max_rooms"),
    Form.max_rooms: (Form.n_bathrooms, "n_bathrooms"),
    Form.n_bathrooms: (Form.furnished, "furnished"),
    Form.furnished: (Form.balcony, "balcony"),
    Form.balcony: (Form.terrace, "terrace"),
    Form.terrace: (Form.pool, "pool"),
    Form.pool: (Form.cellar, "cellar"),
    Form.cellar: (Form.prepare_for_search, "prepare_url"),
}

class SearchParamsHandlers():

    def __init__(self, loader: ComponentsLoader, search_service: SearchService):
        self.loader = loader
        self.search_service = search_service

    async def set_search_filters(self, message: Message, state: FSMContext):
        await message.answer(
            await self.loader.get_message_template(state, "start"),
            reply_markup=await self.loader.create_inline_keyboard_button_markup(
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
        await message.answer(await self.loader.get_message_template(state, "get_max_price"),
                             reply_markup=await self.add_navigation_buttons(state))

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
        await message.answer(text=await self.loader.get_message_template(state, "get_min_rooms"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_min_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(min_rooms=callback_query.data)
        await state.set_state(Form.max_rooms)
        await self.max_rooms(callback_query.message, state)

    async def max_rooms(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4","5"])
        await message.answer(text=await self.loader.get_message_template(state, "get_max_rooms"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_max_rooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(max_rooms=callback_query.data)
        await state.set_state(Form.n_bathrooms)
        await self.n_bathrooms(callback_query.message, state)

    async def n_bathrooms(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_markup_from_template(["1","2","3","4"])
        await message.answer(text=await self.loader.get_message_template(state, "get_n_bathrooms"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_n_bathrooms(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(bathrooms=callback_query.data)
        await state.set_state(Form.furnished)
        await self.furnished(callback_query.message, state)

    async def furnished(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state,"yes_no"))
        await message.answer(text=await self.loader.get_message_template(state, "get_furnished"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_furnished(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(furnished=callback_query.data)
        await state.set_state(Form.balcony)
        await self.balcony(callback_query.message, state)

    async def balcony(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state,"yes_no"))
        await message.answer(text=await self.loader.get_message_template(state, "get_balcony"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_balcony(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(balcony=callback_query.data)
        await state.set_state(Form.terrace)
        await self.terrace(callback_query.message, state)

    async def terrace(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state,"yes_no"))
        await message.answer(text=await self.loader.get_message_template(state, "get_terrace"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_terrace(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(terrace=callback_query.data)
        await state.set_state(Form.pool)
        await self.pool(callback_query.message, state)

    async def pool(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state,"yes_no"))
        await message.answer(text=await self.loader.get_message_template(state, "get_pool"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_pool(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(pool=callback_query.data)
        await state.set_state(Form.cellar)
        await self.cellar(callback_query.message, state)

    async def cellar(self, message: Message, state: FSMContext):
        keyboard_markup = self.loader.create_inline_keyboard_buttons_with_callback(
            await self.loader.get_keyboard_button_template(state,"yes_no"))
        await message.answer(text=await self.loader.get_message_template(state, "get_cellar"),
                             reply_markup=await self.add_navigation_buttons(state,keyboard_markup))

    async def handle_cellar(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(cellar=callback_query.data)
        await state.set_state(Form.prepare_for_search)
        await self.prepare_for_search(callback_query, state)

    async def add_navigation_buttons(self, state: FSMContext, keyboard_markup = None):
        keyboard_markup = await self.loader.append_button_to_markup(
            await self.loader.get_keyboard_button_template(state,"go_prev_step"),"go_prev_step",keyboard_markup)
        return await self.loader.add_skip_buttons(state, keyboard_markup)
    
    async def handle_go_prev_step(self, callback_query: CallbackQuery, state: FSMContext):
        await self.handle_state_transition(callback_query, state, PREV_STEP_TRANSITIONS)
    
    async def handle_skip_step(self, callback_query: CallbackQuery, state: FSMContext):
        await self.handle_state_transition(callback_query, state, SKIP_STEP_TRANSITIONS)

    async def handle_state_transition(self, callback_query: CallbackQuery, state: FSMContext, transition_map: dict):
        current_state = await state.get_state()
        if current_state in transition_map:
            next_state, handler_name = transition_map[current_state]
            await state.set_state(next_state)
            handler = getattr(self, handler_name)
            await handler(callback_query.message, state)

    async def handle_go_to_search(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.prepare_for_search)
        #await self.prepare_for_search(callback_query, state)

    def preprocess_input_data(self,data: dict) -> dict:
        boolean_fields = ['furnished', 'balcony_or_terrace', 'balcony', 'terrace', 'piscina', 'cellar', 'pool']
        for field in boolean_fields:
            if field in data: ## We process it only if its true, if false then we remove it from params
                if data[field].lower() in ['true']:
                    data[field] = True
                elif data[field].lower() in ['false']:
                    del data[field]
                else:
                    data[field] = None  # or raise an error if you want strict validation
        return data
    
    async def prepare_for_search(self, callback_query: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        processed_user_data = self.preprocess_input_data(user_data)
        search_params = SearchParams(**processed_user_data)
        user_id = callback_query.from_user.id
        await self.search_service.prepare_for_search(state, user_id, search_params)

    async def start_searching(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(start_searching=True)
        await state.set_state(Form.searching)
        
    async def stop_searching(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(stop_searching=True)
        await state.set_state(Form.end)

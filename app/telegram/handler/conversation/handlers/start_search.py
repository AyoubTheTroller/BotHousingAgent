from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.telegram.loader.conversation_loader import ConversationLoader
from app.service.search.search_service import SearchService

class Form(StatesGroup):
    searching = State()
    using_filter = State()
    use_new_filters = State()
    ask_for_filters_type = State()
    show_saved_filters = State()
    end = State()

class StartSearchHandlers:

    def __init__(self, loader: ConversationLoader, search_service: SearchService):
        self.loader = loader
        self.search_service = search_service

    async def start_home_search(self, message: Message, state: FSMContext):
        user = await self.search_service.get_user(state)
        command_parts = message.text.split()
        if len(command_parts) > 1:
            filters_name = command_parts[1]
            await self.set_search_params(message.from_user.id, filters_name, state)
        elif user.search_params:
            await self.ask_user_for_search_params(message, state)
        else:
            await self.search_service.add_new_search_filters(message, state)

    async def start_search_with_callback(self, callback_query: CallbackQuery, state: FSMContext):
        await self.start_search(callback_query.from_user.id,state)

    async def set_search_params(self, user_id, filters_name, state: FSMContext):
        await state.set_state(Form.using_filter)
        search_params = await self.search_service.load_search_params(filters_name,state)
        await state.update_data(search_params=search_params)
        await self.start_search(user_id,state)

    async def stop_search_with_command(self, message: Message, state: FSMContext):
        await self.stop_search(message,state)

    async def stop_search_with_callback(self, callback_query: CallbackQuery, state: FSMContext):
        await self.stop_search(callback_query.message,state)

    async def stop_search(self, message: Message, state: FSMContext):
        await state.update_data(stop_search=True)
        current_state = await state.get_state()
        if current_state == Form.searching:
            await message.answer(text=await self.loader.get_message_template(state, "stopping_search"))
            await state.set_state(Form.end)
        else:
            await message.answer(text=await self.loader.get_message_template(state, "no_active_search"))

    async def start_search(self, user_id, state: FSMContext):
        await state.update_data(stop_search=False)
        await state.set_state(Form.searching)
        await self.search_service.prepare_for_search(user_id, state)
        await self.search_service.start_search(state)
        await state.set_state(Form.end)

    async def ask_user_for_search_params(self, message: Message, state: FSMContext):
        await state.set_state(Form.ask_for_filters_type)
        text = await self.loader.get_message_template(state,"search_filters")
        keyboard = await self.loader.append_button_to_markup(
            text=await self.loader.get_keyboard_button_template(state,"use_new_filters"),
            callback_data="use_new_filters")
        keyboard = await self.loader.append_button_to_markup(
            text=await self.loader.get_keyboard_button_template(state,"show_saved_filters"),
            callback_data="show_saved_filters",
            keyboard_markup=keyboard)
        await message.answer(text,reply_markup=keyboard)

    async def use_new_filters(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.use_new_filters)
        await self.search_service.add_new_search_filters(callback_query.message, state)

    async def start_search_using_filters(self, callback_query: CallbackQuery, state: FSMContext):
        filters_name = callback_query.data.replace("start_search_using_filters_", "", 1)
        await self.set_search_params(callback_query.from_user.id,filters_name,state)
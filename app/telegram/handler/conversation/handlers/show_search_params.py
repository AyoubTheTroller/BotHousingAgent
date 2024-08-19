from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.telegram.loader.conversation_loader import ConversationLoader
from app.service.search.search_service import SearchService

class Form(StatesGroup):
    show_saved_filters = State()
    remove_filters = State()
    end = State()

class ShowSearchParamsHandlers:

    def __init__(self, loader: ConversationLoader, search_service: SearchService):
        self.loader = loader
        self.search_service = search_service
    
    async def show_saved_filters_command(self, message: Message, state: FSMContext):
        await self.show_saved_filters(message,state)
    
    async def show_saved_filters_callback(self, callback_query: CallbackQuery, state: FSMContext):
        await self.show_saved_filters(callback_query.message,state)

    async def show_saved_filters(self, message: Message, state: FSMContext):
        await state.set_state(Form.show_saved_filters)
        await message.answer(text=await self.loader.get_message_template(state,"saved_filters"))
        saved_search_params = await self.search_service.get_user_search_params(state)
        for filters_name, search_params in saved_search_params.items():
            text, keyboard = await self.loader.create_saved_search_params_card(language=await self.search_service.get_from_state(state,"language"),
                                                                         search_params_name=filters_name,
                                                                         search_params=search_params)
            await message.answer(text=text, reply_markup=keyboard)

    async def remove_search_params(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.remove_filters)
        filters_name = callback_query.data.replace("remove_search_filters_", "", 1)
        text = await self.loader.get_message_template(state,"delete_confirmation",filters_name=filters_name)
        keyboard = await self.loader.append_button_to_markup(
            text=await self.loader.get_keyboard_button_template(state,"yes",),
            callback_data="delete_filters_"+filters_name
        )
        keyboard = await self.loader.append_button_to_markup(
            text=await self.loader.get_keyboard_button_template(state,"no",),
            callback_data="keep_filters",
            keyboard_markup=keyboard
        )
        await callback_query.message.answer(text=text, reply_markup=keyboard)
    
    async def handle_delete_filters(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.edit_reply_markup(reply_markup=None)
        filters_name = callback_query.data.replace("delete_filters_", "", 1)
        await self.search_service.remove_user_filters_by_name(state,filters_name)
        await callback_query.message.answer(text=await self.loader.get_message_template(state,"successfull_removal",filters_name=filters_name))
        await state.set_state(Form.show_saved_filters)

    async def handle_keep_filters(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await state.set_state(Form.show_saved_filters)
        await callback_query.message.answer(text=await self.loader.get_message_template(state,"cancelled_removal"))
        
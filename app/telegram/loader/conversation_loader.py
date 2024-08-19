from aiogram.fsm.context import FSMContext
from app.telegram.loader.components_loader import ComponentsLoader
from app.scraping.model.search_params import SearchParams

class ConversationLoader(ComponentsLoader):

    async def add_skip_buttons(self, state: FSMContext, keyboard_markup = None, last = False):
        skip_step = await self.get_keyboard_button_template(state, "skip_step")
        review_params = await self.get_keyboard_button_template(state, "review_params")
        if not last:
            keyboard_markup = await self.append_button_to_markup(skip_step,"skip_step",keyboard_markup)
        keyboard_markup = await self.append_button_to_markup(review_params,"review_params",keyboard_markup)
        return keyboard_markup

    async def create_params_message(self, search_params: SearchParams, language: str) -> str:
        fields = search_params.to_clean_dict()
        fields["search_type"] = await self.get_message_template_by_lang(language,fields["search_type"])
        true = await self.get_message_template_by_lang(language, "true")
        false = await self.get_message_template_by_lang(language, "false")
        for key, value in fields.items():
            if value is True:
                fields[key] = true
            elif value is False:
                fields[key] = false
        message_parts = []
        for key, value in fields.items():
            if value is not None:
                message_part = await self.get_message_template_by_lang(language, key, **{key: value})
                message_parts.append(message_part)

        return ''.join(filter(None, message_parts))

    async def create_review_params_message(self, state: FSMContext, search_params: SearchParams):
        language = await self.get_language(state)
        message_parts = []
        message_parts.append(await self.get_message_template_by_lang(language,"filters"))
        message_parts.append(await self.create_params_message(search_params,language))
        return ''.join(filter(None, message_parts))

    async def add_review_params_buttons(self, state: FSMContext, keyboard_markup = None):
        save_search_params = await self.get_keyboard_button_template(state,"save_search_params")
        start_search = await self.get_keyboard_button_template(state,"start_search")
        keyboard_markup = await self.append_button_to_markup(save_search_params,"save_search_params",keyboard_markup)
        keyboard_markup = await self.append_button_to_markup(start_search,"start_search",keyboard_markup)
        return keyboard_markup
    
    async def create_saved_search_params_card(self, language, search_params_name, search_params):
        """Returns a tuple containing the card message and card buttons markup"""
        message_parts = []
        message_parts.append(await self.get_message_template_by_lang(language,"filters_name",filters_name=search_params_name))
        message_parts.append(await self.create_params_message(search_params,language))
        keyboard_markup = await self.append_button_to_markup(
            text=await self.get_keyboard_button_template_by_lang(language,"start_search"),
            callback_data="start_search_using_filters_"+search_params_name)
        keyboard_markup = await self.append_button_to_markup(
            text=await self.get_keyboard_button_template_by_lang(language,"delete_filters"),
            callback_data="remove_search_filters_"+search_params_name,
            keyboard_markup=keyboard_markup)
        return (''.join(filter(None, message_parts)),keyboard_markup)

from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,InputMediaPhoto
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from app.service.template.telegram.template_service import TelegramTemplateService
from app.scraping.model.listing import Listing

class ComponentsLoader():
    def __init__(self,
                 template_service: TelegramTemplateService,
                 interaction_type: str,
                 handler_type: str):

        self.template_service = template_service
        self.interaction_type = interaction_type
        self.handler_type = handler_type
    
    async def get_message_template(self, state: FSMContext, *keys,  **kwargs):
        """Helper function to return the message from a template."""
        user_data = await state.get_data()
        language = user_data.get('language')
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)
    
    async def get_message_template_with_lang(self, language, *keys, **kwargs):
        """Helper function to return the message from a template."""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "message", *keys, **kwargs)
    
    async def get_keyboard_button_template(self, state: FSMContext, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        user_data = await state.get_data()
        language = user_data.get('language')
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)
    
    async def get_keyboard_button_template_with_lang(self, language, *keys, **kwargs):
        """Helper function to return the array of keyboard templates"""
        return await self.template_service.render_template(language, self.interaction_type, self.handler_type, "button", *keys, **kwargs)

    async def create_inline_keyboard_button_markup(self, button_text: str, callback_data) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from one button data.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data=callback_data)]]
        )
        return keyboard

    def create_inline_keyboard_buttons_markup_from_template(self, buttons: List) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=text)] for text in buttons]
        )
        return keyboard
    
    def create_inline_keyboard_buttons_with_callback(self, buttons: List) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data.
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for button in buttons:
            text, callback_data = self.split_button_data(button)
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

        return keyboard
    
    def split_button_data(self, button: str) -> Tuple[str,str]:
        """returns button data as tuple, one part is the text shown the other is the callback data """
        parts = button.split('.')
        if len(parts) == 2:
            return parts[0], parts[1]
        
    def create_inline_keyboard_buttons_markup(self, buttons: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup from a list of button data represented as tuples.
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text, callback_data=callback)]
                for text, callback in buttons
            ]
        )
        return keyboard

    def create_keyboard_buttons_markup(self, buttons: List) -> ReplyKeyboardMarkup:
        """
        Creates a reply keyboard markup from a list of buttons
        """
        markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = button) for button in buttons]],
                                     resize_keyboard=True,
                                     one_time_keyboard=False)
        return markup

    async def append_button_to_markup(self, text, callback_data, keyboard_markup = None) -> InlineKeyboardMarkup:
        if keyboard_markup is None:
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
        return keyboard_markup

    async def add_skip_buttons(self, state: FSMContext, keyboard_markup = None) -> InlineKeyboardMarkup:
        skip_step = await self.get_keyboard_button_template(state, "skip_step")
        go_to_search = await self.get_keyboard_button_template(state, "go_to_search")
        if keyboard_markup is None:
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=skip_step, callback_data="skip_step")])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=go_to_search, callback_data="go_to_search")])
        return keyboard_markup

    async def load_listing_photos(self, listing: Listing) -> List[InputMediaPhoto]:
        max_photos = 8  # Maximum set in order to manage telegram flood control with mediagroups
        if listing.photos_url:
            truncated_photos = listing.photos_url[:max_photos]
            return [InputMediaPhoto(media=url) for url in truncated_photos]
        else:
            return None

    async def load_listing_with_keyboard(self, listing: Listing, language: str) -> InlineKeyboardMarkup:
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard_markup.inline_keyboard.append([InlineKeyboardButton(
            text=await self.get_keyboard_button_template_with_lang(language, "view_details"), url=listing.url)])
        if listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=f"+39 {phone}", callback_data=f"contact_{phone}")])
        elif listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=f"+39 {phone}", callback_data=f"contact_{phone}")])
        elif listing.private_phone:
            keyboard_markup.inline_keyboard.append([InlineKeyboardButton(
                          text=await self.get_keyboard_button_template_with_lang(language, "view_private_phone"), url=listing.private_phone)])
        return keyboard_markup
    
    async def load_listing_message(self, listing: Listing, language: str) -> str:
        fields = {
            "title": listing.title if listing.title else None,
            "price_formatted": listing.price_formatted if listing.price_formatted else None,
            "city_name": listing.city_name if listing.city_name else None,
            "city_zone": listing.city_zone if listing.city_zone else None,
            "bathrooms": listing.bathrooms if listing.bathrooms is not None else None,
            "rooms": listing.rooms if listing.rooms is not None else None,
            "bedrooms": listing.bedrooms if listing.bedrooms is not None else None,
            "surface": listing.surface if listing.surface is not None else None,
            "agency_name": listing.agency_name if listing.agency_name else None,
            "agent_name": listing.agent_name if listing.agent_name else None,
        }
        message_parts = []
        # Populate the message with non-empty fields
        for key, value in fields.items():
            if value is not None:
                template_key = f"listing_{key}"
                message_part = await self.get_message_template_with_lang(language, template_key, **{key: value})
                message_parts.append(message_part)

        # Handling phone numbers
        if listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    message_parts.append(await self.get_message_template_with_lang(language, "listing_agency_phone", agency_phone=phone))
        elif listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    message_parts.append(await self.get_message_template_with_lang(language, "listing_agent_phone", private_phone=phone))

        return ''.join(filter(None, message_parts))
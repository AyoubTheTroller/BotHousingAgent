from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,InputMediaPhoto
from app.scraping.model.listing import Listing
from app.telegram.loader.components_loader import ComponentsLoader

class SearchLoader(ComponentsLoader):

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
            text=await super().get_keyboard_button_template_by_lang(language, "view_details"), url=listing.url)])
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
                          text=await super().get_keyboard_button_template_by_lang(language, "view_private_phone"), url=listing.private_phone)])
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
                message_part = await super().get_message_template_by_lang(language, template_key, **{key: value})
                message_parts.append(message_part)

        # Handling phone numbers
        if listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    message_parts.append(await super().get_message_template_by_lang(language, "listing_agency_phone", agency_phone=phone))
        elif listing.agency_phones:
            for phone in listing.agency_phones:
                if phone is not None:
                    message_parts.append(await super().get_message_template_by_lang(language, "listing_agent_phone", private_phone=phone))

        return ''.join(filter(None, message_parts))
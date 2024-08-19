from aiogram import Bot
from aiogram.fsm.context import FSMContext
from app.telegram.loader.search_loader import SearchLoader
from app.service.mongodb.dao.user.user_dao import UserDAO

class SearchEvents:
    def __init__(self, loader: SearchLoader, user_dao: UserDAO, bot: Bot):
        self.loader = loader
        self.user_dao = user_dao
        self.bot = bot

    async def prepare_for_search(self, event_data: dict) -> None:
        text = await self.loader.get_keyboard_button_template_by_lang(event_data['language'],"stop_search")
        keyboard_markup = await self.loader.append_button_to_markup(text,"stop_search")
        await self.bot.send_message(chat_id=event_data['user_id'],
                                    text=await self.loader.get_message_template_by_lang(event_data['language'], "url_link", url=event_data['url']),
                                    reply_markup=keyboard_markup)
        await self.bot.send_message(chat_id=event_data['user_id'], text=await self.loader.get_message_template_by_lang(event_data['language'], "searching"))

    async def no_listings_found(self, event_data: dict) -> None:
        await self.bot.send_message(chat_id=event_data['user_id'],
                                    text= await self.loader.get_message_template_by_lang(event_data['language'], "no_listings_found"))
    
    async def stop_search(self, event_data: dict):
        await self.bot.send_message(chat_id=event_data['user_id'],
                                    text= await self.loader.get_message_template_by_lang(event_data['language'], "search_stopped"))
        
    async def new_listing_found(self, event_data: dict) -> None:
        listing = event_data["listing"]
        language = event_data["language"]
        user_id = event_data["user_id"]
        media_group = await self.loader.load_listing_photos(listing)
        keyboard = await self.loader.load_listing_with_keyboard(listing, language)
        message_text = await self.loader.load_listing_message(listing, language)
        if media_group is not None:
            await self.bot.send_media_group(chat_id=user_id, media=media_group)
        await self.bot.send_message(chat_id=user_id,text=message_text,reply_markup=keyboard, parse_mode="HTML")

    async def search_completed(self, event_data: dict) -> None:
        await self.bot.send_message(chat_id=event_data['user_id'],
                                    text= await self.loader.get_message_template_by_lang(event_data['language'], "search_completed"))

    
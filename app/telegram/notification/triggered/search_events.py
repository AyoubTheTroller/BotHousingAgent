from aiogram import Bot
from app.telegram.loader.search_loader import SearchLoader
from app.service.mongodb.dao.user.user_dao import UserDAO

class SearchEvents:
    def __init__(self, loader: SearchLoader, user_dao: UserDAO, bot: Bot):
        self.loader = loader
        self.user_dao = user_dao
        self.bot = bot

    async def new_listing_found(self, event_data: dict) -> None:
        user_language = await self.user_dao.get_user_language_by_id(event_data['user_id'])
        listing = event_data['listing']
        message = "Listing"
        await self.bot.send_message(chat_id=event_data['user_id'], text=message)
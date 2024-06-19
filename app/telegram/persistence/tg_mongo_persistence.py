from typing import Dict
from telegram.ext import BasePersistence

class TelegramMongoPersistence(BasePersistence):
    """Persistence adapter for storing data in MongoDB."""

    def __init__(self, mongo_service):
        super().__init__()
        self.db_service = mongo_service

    async def get_user_data(self) -> Dict[int, Dict]:
        """Gets all user data from MongoDB."""
        user_data_dict = await self.db_service.get_all_user_data()
        return user_data_dict

    async def update_user_data(self, user_id: int, data: Dict) -> None:
        """Updates user data in MongoDB."""
        await self.db_service.update_user_data(user_id, data)

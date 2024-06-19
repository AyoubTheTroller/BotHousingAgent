from typing import Dict
from app.service.mongodb.dao.base_dao import BaseDAO
from app.service.mongodb.mongo_service import MongoService

class UserDAO(BaseDAO):
    """DAO for interacting with the user collection."""

    def __init__(self, mongo_service: MongoService, db_alias: str, collection_name: str):
        super().__init__(mongo_service, db_alias)
        self.collection = self.mongo_service.get_collection(db_alias, collection_name)

    async def get_user_data(self, user_id: int) -> dict:
        """Retrieves user data from MongoDB."""
        result = await self.collection.find_one({"_id": user_id})
        return result.get("data", {}) if result else {}

    async def update_user_data(self, user_id: int, data: dict) -> None:
        """Updates user data in MongoDB."""
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"data": data}},
            upsert=True
        )
        
    async def get_all_user_data(self) -> Dict[int, Dict]:
        """Retrieves all user data from MongoDB."""
        user_data = {}
        async for user in self.collection.find():
            user_id = user["_id"]
            user_data[user_id] = user["data"]
        return user_data

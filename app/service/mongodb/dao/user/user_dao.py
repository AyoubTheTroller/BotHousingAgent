from datetime import datetime
from pymongo.collection import Collection
from app.telegram.model.user import User

class UserDAO:
    def __init__(self, collection: Collection):
        self._collection = collection

    async def get_user_by_id(self, user_id: int) -> User:
        user_data = await self._collection.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    async def get_user_by_username(self, username: str) -> User:
        user_data = await self._collection.find_one({"username": username})
        if user_data:
            return User(**user_data)
        return None
    
    async def get_user_language_by_id(self, user_id: int) -> str:
        user_data = await self._collection.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data).language
        return None

    async def add_user(self, user: User) -> None:
        await self._collection.update_one(
            {"user_id": user.user_id},
            {"$set": user.model_dump()},
            upsert=True
        )

    async def update_user_language(self, user_id: int, language) -> None:
        await self._collection.update_one(
            {"user_id": user_id},
            {"$set": {"language": language}}
        )


    async def update_user_activity(self, user_id: int) -> None:
        await self._collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.now().isoformat()}}
        )

    async def update_user_authorization(self, user_id: int, authorized: bool) -> None:
        await self._collection.update_one(
            {"user_id": user_id},
            {"$set": {"authorized": authorized}}
        )

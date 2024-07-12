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

    async def add_user(self, user: User) -> None:
        self._collection.update_one(
            {"user_id": user.user_id},
            {"$set": user.model_dump()},
            upsert=True
        )

    async def update_user_activity(self, user_id: int) -> None:
        self._collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.utcnow().isoformat()}}
        )

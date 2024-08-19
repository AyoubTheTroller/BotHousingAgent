from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.telegram.model.user import User
from app.service.mongodb.dao.base_dao import BaseDAO

class UserDAO(BaseDAO[User]):

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_data = await self._collection.find_one({"username": username})
        if user_data:
            return self._convert_to_model(user_data)
        return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user_data = await self._collection.find_one({"id": user_id})
        if user_data:
            return self._convert_to_model(user_data)
        return None
    
    async def get_user_language_by_id(self, user_id: int) -> Optional[str]:
        user = await self.get_user_by_id(user_id)
        if user:
            return user.language
        return None

    async def add_user(self, user: User) -> None:
        await self._collection.update_one(
            {"id": user.id},
            {"$set": self._convert_to_dict(user)},
            upsert=True
        )

    async def update_user_language(self, user_id: int, language: str) -> None:
        await self.update_with_user_id(user_id,{"language" : language})

    async def update_user_activity(self, user_id: int) -> None:
        await self.update_with_user_id(user_id,{"last_active": datetime.now().isoformat()})

    async def update_user_authorization(self, user_id: int, authorized: bool) -> None:
        await self.update_with_user_id(user_id,{"authorized": authorized})

    async def update_with_user_id(self, user_id, data):
        await self._collection.update_one(
            {"id": user_id},
            {"$set": data}
        )

    async def update_search_params(self, native_id: ObjectId, key: str, value: str) -> None:
        update_operation = {"$set": {f"search_params.{key}": value}}
        await self.update_field(native_id, update_operation)
    
    async def remove_search_param(self, native_id: ObjectId, key: str) -> None:
        update_operation = {"$unset": {f"search_params.{key}": ""}}
        await self.update_field(native_id, update_operation)

    def _convert_to_model(self, data: dict) -> User:
        return User(**data)

    def _convert_to_dict(self, model: User) -> dict:
        return model.model_dump()

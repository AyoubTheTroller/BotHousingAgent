from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from pymongo.collection import Collection

T = TypeVar('T') # For generic models

class BaseDAO(ABC, Generic[T]):
    def __init__(self, collection: Collection):
        self._collection = collection

    async def get_by_id(self, id: int) -> Optional[T]:
        data = await self._collection.find_one({"id": id})
        if data:
            return self._convert_to_model(data)
        return None

    async def add(self, model: T) -> None:
        await self._collection.update_one(
            {"id": model.id},
            {"$set": self._convert_to_dict(model)},
            upsert=True
        )

    async def update(self, id: int, update_data: dict) -> None:
        await self._collection.update_one(
            {"id": id},
            {"$set": update_data}
        )

    @abstractmethod
    def _convert_to_model(self, data: dict) -> T:
        pass

    @abstractmethod
    def _convert_to_dict(self, model: T) -> dict:
        pass

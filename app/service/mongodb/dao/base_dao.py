from abc import ABC, abstractmethod
from typing import AsyncGenerator, TypeVar, Generic, Optional
from bson import ObjectId
from pymongo.collection import Collection

T = TypeVar('T')  # For generic models

class BaseDAO(ABC, Generic[T]):
    def __init__(self, collection: Collection):
        self._collection = collection

    async def create_with_id(self, model: T) -> ObjectId:
        """Creates a new document with a MongoDB-generated ObjectId."""
        document = self._convert_to_dict(model)
        result = await self._collection.insert_one(document)
        return result.inserted_id

    async def add_with_hash_id(self, model: T, hash_id: str) -> None:
        await self._collection.update_one(
            {"hash_id": hash_id},
            {"$set": self._convert_to_dict(model)},
            upsert=True
        )

    async def get_by_hash_id(self, hash_id: str) -> Optional[T]:
        data = await self._collection.find_one({"hash_id": hash_id})
        if data:
            return self._convert_to_model(data)
        return None

    async def get_by_id(self, _id: ObjectId) -> Optional[T]:
        data = await self._collection.find_one({"_id": _id})
        if data:
            return self._convert_to_model(data)
        return None

    async def add(self, model: T) -> None:
        await self._collection.update_one(
            {"_id": model.native_id},
            {"$set": self._convert_to_dict(model)},
            upsert=True
        )

    def _to_object_id(self, _id: str) -> ObjectId:
        """Converts a string ID to a MongoDB ObjectId."""
        return ObjectId(_id)

    async def update(self, _id: ObjectId, update_data: dict) -> None:
        """Updates the document with the provided data."""
        await self._collection.update_one(
            {"_id": _id},
            {"$set": update_data}
        )

    async def update_field(self, _id: ObjectId, update_operation: dict) -> None:
        """Updates specific fields using MongoDB update operators."""
        await self._collection.update_one(
            {"_id": _id},
            update_operation
        )

    async def update_push(self, _id: ObjectId, update_data: dict) -> None:
        """Pushes values to an array field in the document."""
        await self._collection.update_one(
            {"_id": _id},
            {"$push": update_data}
        )

    async def update_pull(self, _id: ObjectId, update_data: dict) -> None:
        """Pulls values from an array field in the document."""
        await self._collection.update_one(
            {"_id": _id},
            {"$pull": update_data}
        )

    async def add_to_set(self, _id: ObjectId, update_data: str) -> None:
        await self._collection.update_one(
            {"_id": _id},
            {"$addToSet": update_data}
        )

    async def get_all_cursor(self) -> AsyncGenerator[dict, None]:
        """Returns a cursor to iterate over all documents in the collection."""
        cursor = self._collection.find({})
        async for document in cursor:
            yield document

    async def count_documents(self, filter: dict = None) -> int:
        """Counts the number of documents in the collection matching the filter."""
        filter = filter or {}
        return await self._collection.count_documents(filter)

    @abstractmethod
    def _convert_to_model(self, data: dict) -> T:
        pass

    @abstractmethod
    def _convert_to_dict(self, model: T) -> dict:
        pass

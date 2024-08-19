from typing import Optional
from app.scraping.model.search_params import SearchParams
from app.service.mongodb.dao.base_dao import BaseDAO

class SearchParamsDAO(BaseDAO[SearchParams]):

    async def get_filters_by_id(self, id: int) -> Optional[SearchParams]:
        return await self.get_by_id(id)

    async def add_search_params(self, search_params: SearchParams) -> str:
        hash_id = search_params.generate_hash_id()
        if await self.get_by_hash_id(hash_id):
            return hash_id
        await self.add_with_hash_id(search_params, hash_id)
        return hash_id

    async def print_all(self) -> None:
        """Retrieves and prints all SearchParams documents."""
        async for document in await self.get_all_cursor():
            model = self._convert_to_model(document)
            print(model)

    def _convert_to_model(self, data: dict) -> SearchParams:
        return SearchParams(**data)

    def _convert_to_dict(self, model: SearchParams) -> dict:
        model = {k: v for k, v in model.model_dump().items() if v is not None}
        return model

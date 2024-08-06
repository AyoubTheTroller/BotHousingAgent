from typing import List
from aiogram.fsm.context import FSMContext
from app.service.scraping.scraping_service import ScrapingService
from app.scraping.model.search_params import SearchParams
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.mongo_service import MongoService

class SearchService:
    
    def __init__(self, scraping_service: ScrapingService,
                       mongo_service: MongoService,
                       event_emitter: EventEmitter):
        self.scraping_service = scraping_service
        self.mongo_service = mongo_service
        self.event_emitter = event_emitter

    async def save_search_params(self, user_id: int, search_params: SearchParams):
        await self.mongo_service.save_search_params(user_id, search_params)

    async def load_search_params(self, user_id: int) -> SearchParams:
        return await self.mongo_service.load_search_params(user_id)

    async def start_search(self, user_id: int, search_params: SearchParams):
        url = await self.scraping_service.build_url(search_params)
        listings = await self.scraping_service.scrape_listings(url)
        await self._trigger_listings_event(user_id, listings)

    async def prepare_for_search(self, state: FSMContext, user_id: int, search_params: SearchParams):
        """This method prepares the url for the search and asks the user to start search"""
        
        pass

    async def _trigger_listings_event(self, user_id: int, listings: List[dict]):
        for listing in listings:
            event_data = {
                'user_id': user_id,
                'listing': listing
            }
            await self.event_emitter.emit("new_listing_found", event_data)

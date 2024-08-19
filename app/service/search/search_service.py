import asyncio
from typing import List, Dict
from aiogram.fsm.context import FSMContext
from app.service.scraping.scraping_service import ScrapingService
from app.scraping.model.search_params import SearchParams
from app.telegram.notification.event_emitter import EventEmitter
from app.service.mongodb.dao.user.user_dao import UserDAO
from app.telegram.model.user import User
from app.service.mongodb.dao.search_params.search_params_dao import SearchParamsDAO

class SearchService:
    
    def __init__(self, scraping_service: ScrapingService,
                       event_emitter: EventEmitter,
                       user_dao: UserDAO,
                       search_params_dao: SearchParamsDAO):
        self.scraping_service = scraping_service
        self.user_dao = user_dao
        self.event_emitter = event_emitter
        self.search_params_dao = search_params_dao

    async def get_from_state(self, state: FSMContext, key):
        data = await state.get_data()
        return data.get(key,None)

    async def set_user(self, user_id: int, state: FSMContext):
        user = await self.get_user(state)
        if user is None:
            user = await self.user_dao.get_user_by_id(user_id)
            await state.update_data(user=user)
            await state.update_data(user_id=user_id)
        return user
    
    async def update_user(self, user_id: int, state: FSMContext):
        user = await self.user_dao.get_user_by_id(user_id)
        await state.update_data(user=user)

    async def get_user(self, state) -> User:
        return await self.get_from_state(state,"user")
    
    async def get_search_params(self, state) -> SearchParams:
        return await self.get_from_state(state,"search_params")
    
    async def save_search_params(self, search_params_key, state: FSMContext):
        user = await self.get_user(state)
        search_params = await self.get_search_params(state)
        hash_id = await self.search_params_dao.add_search_params(search_params)
        await self.user_dao.update_search_params(user.native_id,search_params_key, hash_id)
        await self.update_user(user.id,state)

    async def remove_user_filters_by_name(self, state: FSMContext,filters_name):
        user = await self.get_user(state)
        if user.get_search_param(filters_name):
            await self.user_dao.remove_search_param(user.native_id,filters_name)
            await self.update_user(user.id,state)

    async def check_custom_name(self, custom_name, state: FSMContext):
        user = await self.get_user(state)
        return user.check_and_sanitize_search_param_name(custom_name)

    async def load_search_params(self, filter_name: int, state: FSMContext) -> SearchParams:
        user = await self.get_user(state)
        hash_id = user.get_search_param(filter_name)
        return await self.search_params_dao.get_by_hash_id(hash_id)

    async def get_user_search_params(self, state: FSMContext) -> Dict[str, SearchParams]:
        user = await self.get_user(state)
        search_params: Dict[str, SearchParams] = {}
        for key, value in user.search_params.items():
            search_params[key] = await self.search_params_dao.get_by_hash_id(value)
        return search_params

    async def start_search(self, state: FSMContext):
        listings = await self.scraping_service.scrape_listings(await self.get_from_state(state,"url"))
        event_data = {
            'user_id': await self.get_from_state(state,"user_id"),
            'language': await self.get_from_state(state,"language")
        }
        if not listings:
            await self.event_emitter.emit("no_listings_found",event_data)
        else:
            await self._trigger_listings_event(state,listings)

    async def prepare_for_search(self, user_id: int, state: FSMContext):
        """This method prepares the url for the search and asks the user to start search"""
        url = await self.scraping_service.build_url(await self.get_from_state(state,"search_params"))
        await state.update_data(url=url)
        await state.update_data(user_id=user_id)
        event_data = {
            'url':url,
            'user_id':user_id,
            'language':await self.get_from_state(state,"language")
        }
        await self.event_emitter.emit("prepare_for_search", event_data)

    async def _trigger_listings_event(self, state, listings: List[dict]):
        event_data = {
            'user_id': await self.get_from_state(state, "user_id"),
            'language': await self.get_from_state(state, "language")
        }
        for listing in listings:
            if await self.get_from_state(state,"stop_search"):
                await self.event_emitter.emit("stop_search", event_data)
                return
            event_data["listing"]=listing
            await self.event_emitter.emit("new_listing_found", event_data)
            await asyncio.sleep(3)
        await self.event_emitter.emit("search_completed", event_data)

    async def add_new_search_filters(self,message,state):
        await self.event_emitter.emit_message("add_search_filters",message,state)

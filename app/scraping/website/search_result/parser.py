import json
from typing import List
from bs4 import BeautifulSoup
from app.scraping.website.base_loader import BaseLoader
from app.scraping.model.listing import Listing

class SearchResultParser():
    def __init__(self, loader: BaseLoader) -> None:
        self.loader = loader
        self.parsing_keys = self.loader.load_json_parsing_keys()

    async def extract_json_from_script(self, soup: BeautifulSoup):
        script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')
        if script_tag:
            return json.loads(script_tag.string)
        return None
    
    async def traverse_data_tree(self, data, *keys):
        """
        Extracts the value from data dictionaries using nested keys.
        Handles both dictionaries and lists.
        """
        for idx, key in enumerate(keys):
            if isinstance(data, dict):
                data = data.get(key, {})
                if data == {}:
                    return None
            elif isinstance(data, list):
                if key == "index":
                    return [await self.traverse_data_tree(item, *keys[idx+1:]) for item in data if item != {}]
                else:
                    index = int(key)
                    if 0 <= index < len(data):
                        data = data[index]
                    else:
                        return None
            else:
                return None
        return data

    async def get_house_listings(self, data):
        listings: list = await self.traverse_data_tree(data, *self.parsing_keys["listings"])
        house_listings: List[Listing] = []
        for listing in listings:
            house_listings.append(await self.populate_listing(listing))
        return house_listings

    async def populate_listing(self, listing) -> Listing:
        listing_data = {}
        for field in Listing.model_fields:
            if field in self.parsing_keys:
                field_value = await self.traverse_data_tree(listing, *self.parsing_keys[field])
                if field_value is not None:
                    listing_data[field] = field_value
        return Listing(**listing_data)
import hashlib
import random
from pydantic import BaseModel

class SearchParams(BaseModel):
    location: str
    search_type: str
    criteria: str = None
    order: str = None
    min_price: int = None
    max_price: int = None
    min_area: int = None
    max_area: int = None
    min_rooms: int = None
    max_rooms: int = None
    bathrooms: int = None
    balcony_or_terrace: bool = None
    balcony: bool = None
    terrace: bool = None
    furnished: bool = None
    piscina: bool = None
    cellar: bool = None
    floor_range: str = None

    def generate_hash_id(self) -> str:
        """Generates a unique hash based on the search parameters, ignoring None values."""
        filtered_params = {k: v for k, v in self.model_dump().items() if v is not None}
        search_params_str = str(sorted(filtered_params.items()))
        return hashlib.sha256(search_params_str.encode()).hexdigest()
    
    def to_clean_dict(self) -> dict:
        """Returns a dictionary representation of the model, excluding None values."""
        return self.model_dump(exclude_none=True)

    def generate_random_name(self) -> str:
        """Generates a custom name using the location and up to two other non-None fields."""
        params = self.to_clean_dict()
        location_short = params.get('location', '')[:6]
        custom_name_parts = [location_short]
        optional_fields = ['max_price', 'min_rooms', 'max_rooms', 'bathrooms']
        additional_parts = [str(params[field]) for field in optional_fields if field in params]
        if additional_parts:
            selected_parts = random.sample(additional_parts, min(2, len(additional_parts)))
            custom_name_parts.extend(selected_parts)

        return "-".join(custom_name_parts)
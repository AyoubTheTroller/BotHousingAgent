from pydantic import BaseModel

class QueryParams(BaseModel):
    city_name: str
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

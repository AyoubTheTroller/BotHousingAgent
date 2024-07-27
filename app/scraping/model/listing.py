from pydantic import BaseModel

class Listing(BaseModel):
    price_formatted: str
    price: int = None
    title: str
    url: str
    agency_name: str = None
    agency_phones: list = None
    agent_name: str = None
    private_phone: str = None
    agent_phones: list = None
    city_name: str = None
    city_zone: str = None
    bathrooms: str = None
    rooms: str = None
    bedrooms: int = None
    surface: str = None
    photos_url: list = None

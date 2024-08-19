from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from bson import ObjectId
from app.telegram.middleware.exception.dao_operations.custom_exceptions import UserUpdateError, UserDataNotFoundError
import re

class User(BaseModel):
    native_id: Optional[ObjectId] = Field(None, alias="_id")
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    authorized: bool
    created_at: datetime
    last_active: datetime
    language: str
    search_params: Dict[str, str] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_serializer('native_id')
    def serialize_id(self, v: ObjectId) -> str:
        return str(v)

    def check_and_sanitize_search_param_name(self, key: str) -> None:
        """Sanitizes the search param key by removing dots and special characters.
           Checks if the sanitized key exists in the user's search_params.
           Raises an exception if the sanitized key is found.
           Returns the sanitized key.
        """
        sanitized_key = re.sub(r'[^a-zA-Z0-9_-]', '', key)
        if sanitized_key in self.search_params:
            raise UserUpdateError(template_key="duplicated_filter_name")
        return sanitized_key

    def get_search_param(self, key: str) -> None:
        """Checks if a search param key exists in the user's search_params.
           Raises a UserDataNotFoundError exception if the key is not found.
        """
        if key not in self.search_params:
            raise UserDataNotFoundError(template_key="search_param_not_found")
        else:
            return self.search_params[key]
        
    def get_search_params(self) -> Dict[str, str]:
        """Returns all search parameters if available.
           Raises a UserDataNotFoundError exception if no search parameters are found.
        """
        if not self.search_params:
            raise UserDataNotFoundError(template_key="no_search_params_saved")
        return self.search_params
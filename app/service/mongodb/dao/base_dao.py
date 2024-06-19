from app.service.mongodb.mongo_service import MongoService

class BaseDAO:
    """Base class for Data Access Objects."""
    def __init__(self, mongo_service: MongoService, db_alias: str):
        self.mongo_service = mongo_service
        self.db_alias = db_alias

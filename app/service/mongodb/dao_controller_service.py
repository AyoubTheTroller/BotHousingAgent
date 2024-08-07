import importlib
from app.mongodb.mongo_client import MongoClient
from app.service.mongodb.mongo_service import MongoService

dao_modules = {
    "UserDAO": "app.service.mongodb.dao.user.user_dao",
}

dao_reference = {
    "users":"UserDAO",
    "admins":"UserDAO",
}

class DaoControllerService(MongoService):
    def __init__(self, mongo_client: MongoClient):
        super().__init__(mongo_client)
        self._daos = {}
        self.create_daos()

    def create_daos(self):
        collections = self.get_all_collections()
        for db_key, collections in collections.items():
            self._daos[db_key] = {}
            for collection_name in collections:
                collection = self.get_database(db_key)[collection_name]
                if collection_name in dao_reference:
                    self._daos[db_key][collection_name] = self.instantiate_dao(dao_reference[collection_name],collection)

    def instantiate_dao(self, dao_class, collection):
        module = importlib.import_module(dao_modules[dao_class])
        class_ = getattr(module, dao_class)
        return class_(collection)

    def get_dao(self, db_key, collection_name):
        return self._daos.get(db_key).get(collection_name, {})

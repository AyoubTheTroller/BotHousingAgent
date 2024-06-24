from app.mongodb.mongo_client import MongoClient

class MongoService():
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client

    def get_collection(self, collection_name):
        return self._mongo_client.get_collection("scraped",collection_name)

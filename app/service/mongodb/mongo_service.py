from app.mongodb.mongo_client import MongoClient

class MongoService():
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client

    def get_scraped_database(self):
        return self._mongo_client.get_database("scraped")
    
    def get_telegram_database(self):
        return self._mongo_client.get_database("telegram")

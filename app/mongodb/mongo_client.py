class MongoClient():
    """ This class provides a base for establishing a MongoDB connection. """
    def __init__(self, client, dbName, collectionName):
        """ Initialize the MongoDB client with the provided client. """
        self.db = client[dbName][collectionName]

    def get_collection(self, database_name, collection_name):
        """ Retrieves a specific collection from the connected database. """
        return self.db[database_name][collection_name]

    def create_collection(self, database_name: str, collection_name: str) -> None:
        """ Creates a new collection in the specified database. """
        database = self.db[database_name]
        database.create_collection(collection_name)

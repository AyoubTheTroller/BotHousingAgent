class MongoClient():
    """Manages multiple MongoDB databases and collections."""

    def __init__(self, client, databases_config: dict):
        """
        Args:
            client: MongoDB client injected.
            databases_config (dict): Configuration of databases and collections.
        """
        self._client = client
        self.databases = {}
        self._initialize_databases(databases_config)

    def _initialize_databases(self, databases_config: dict):
        """Initializes databases and their collections based on configuration."""
        for db_alias, db_config in databases_config.items():
            self.databases[db_alias] = {}
            print(self.databases)
            self.databases[db_alias]["db_name"] = db_config.get("db_name")
            print(self.databases)
            db = self._client[db_config.get("db_name")]
            collections = {}
            for collection in db_config.get("collections"):
                print(collection)
                collections[collection] = db[collection]
            self.databases[db_alias]["collections"] = collections

    def get_databases(self):
        return self.databases

    def get_collection(self, db_alias: str, collection_name: str):
        """Retrieves a specific collection from the specified database."""
        return self.databases[db_alias]["collections"][collection_name]

    # Keep create_collection if you still need it 
    # (though it's often not necessary as collections are created implicitly)
    def create_collection(self, database_name: str, collection_name: str) -> None:
        """
        Creates a new collection in the specified database.

        Args:
            database_name (str): The name of the database.
            collection_name (str): The name of the collection.
        """
        self.databases[database_name].create_collection(collection_name)

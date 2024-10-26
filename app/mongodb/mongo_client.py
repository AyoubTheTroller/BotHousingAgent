import logging

class MongoClient():
    """Manages multiple MongoDB databases and collections."""

    def __init__(self, client, databases_config: dict):
        """
        Args:
            client: MongoDB client injected.
            databases_config (dict): Configuration of databases and collections.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self._client = client
        self._databases = {}
        self._initialize_databases(databases_config)

    def _initialize_databases(self, databases_config: dict):
        """Initializes databases and their collections based on configuration."""
        self.logger.info("Databases Initialization")
        for db_alias, db_config in databases_config.items():
            self._databases[db_alias] = {}
            self._databases[db_alias]["db_name"] = db_config.get("db_name")
            self.logger.info("Added database %s", db_config.get("db_name"))
            db = self._client[db_config.get("db_name")]
            collections = {}
            for collection in db_config.get("collections"):
                collections[collection] = db[collection]
                self.logger.info("Retrieved collection %s", collection)
            self._databases[db_alias]["collections"] = collections
        self.logger.info("Databases Initialization Completed")

    def get_collection(self, db_alias: str, collection_name: str):
        """Retrieves a specific collection from the specified database."""
        return self._databases[db_alias]["collections"][collection_name]

    def get_database(self, db_alias: str):
        return self._databases[db_alias]["collections"]
    
    def get_all_collections(self):
        """Retrieves all collections from all databases."""
        all_collections = {}
        for db_alias, db_info in self._databases.items():
            all_collections[db_alias] = list(db_info["collections"].keys())
        return all_collections
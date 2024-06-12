from dependency_injector import containers, providers
from pymongo import MongoClient as MongoLibrary

class DbContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    database_client = providers.Singleton(MongoLibrary, config.database.mongodb_uri)

    db_mongo = providers.Factory(MongoLibrary, client=database_client, dbName='ScrapedProperties', collectionName='urls_collection')

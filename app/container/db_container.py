from dependency_injector import containers, providers
from pymongo import MongoClient as MongoLibrary
from app.mongodb.mongo_client import MongoClient

class DbContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    mongo_instance = providers.Singleton(MongoLibrary, config.db_client.mongodb_uri)

    mongo_client = providers.Factory(MongoClient, client=mongo_instance, databases_config=config.db_client.databases)

from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient as MongoLibrary
from app.mongodb.mongo_client import MongoClient

class DbContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    # Create the synchronous MongoClient instance
    mongo_instance = providers.Singleton(MongoLibrary, config.db_client.mongodb_uri)

    # Create an AsyncIOMotorClient using the existing synchronous client
    async_mongo_client = providers.Singleton(
        AsyncIOMotorClient,
        config.db_client.mongodb_uri
    )

    # Use the AsyncIOMotorClient in your MongoClient instance
    mongo_client = providers.Singleton(
        MongoClient,
        client=async_mongo_client,
        databases_config=config.db_client.databases
    )

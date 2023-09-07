from config import config

import pymongo
import cache

# MongoDB
MONGODB_HOST = config.get("mongodb")['host']
MONGODB_DATABASE = config.get("mongodb")['database']
MONGODB_COLLECTION_CACHE = config.get("mongodb")['cache_collection']

# подключаемся к БД
MONGODB_CLIENT = pymongo.MongoClient(MONGODB_HOST)

cache_requests = cache.Cache_requests(
    based_url = "http://127.0.0.1:8080",
    timeout = "3",
    ping_url = "/ping",
    collection = MONGODB_CLIENT[MONGODB_DATABASE][MONGODB_COLLECTION_CACHE]
)

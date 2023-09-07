import time
import random

# from fastapi import *
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import deco
import cache
from globals import *

security = HTTPBearer()

@cache.cache_decorator(secure=True)
@deco.try_decorator
async def test_secure(time_sleep: float, credentials: HTTPAuthorizationCredentials = Depends(security)):
    time.sleep(time_sleep)
    return {"number": random.random()}

@cache.cache_decorator(life_hours=0)
@deco.try_decorator
async def test_zero_life(time_sleep: float):
    time.sleep(time_sleep)
    return {"number": random.random()}

@cache.cache_decorator()
@deco.try_decorator
async def test(time_sleep: float):
    time.sleep(time_sleep)
    return {"number": random.random()}

@deco.try_decorator
async def clear_mongo():
    database = MONGODB_CLIENT[MONGODB_DATABASE]
    collection = database[MONGODB_COLLECTION_CACHE]
    collection.drop()
    return {"status": True}

################################################################################

@deco.try_decorator
async def hello(name: str):
    return cache_requests.send(
        method = "GET",
        url = "/hello?name=%s" % (name)
    )

@deco.try_decorator
async def div(a: int, b: int):
    return cache_requests.send(
        method = "POST",
        url = "/div?a=%d&b=%d" % (a, b)
    )

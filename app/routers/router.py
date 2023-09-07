from fastapi import APIRouter
from .test import *

router = APIRouter()

router.add_api_route(
    "/test_secure",
    test_secure,
    methods=['POST'],
    tags=['TEST'],
    description=""
)

router.add_api_route(
    "/test",
    test,
    methods=['POST'],
    tags=['TEST'],
    description=""
)

router.add_api_route(
    "/test_zero_life",
    test_zero_life,
    methods=['POST'],
    tags=['TEST'],
    description=""
)

router.add_api_route(
    "/clear_mongo",
    clear_mongo,
    methods=['POST'],
    tags=['MONGODB'],
    description=""
)

################################################################################

router.add_api_route(
    "/hello",
    hello,
    methods=['GET'],
    tags=['TEST REQUESTS'],
    description=""
)

router.add_api_route(
    "/div",
    div,
    methods=['POST'],
    tags=['TEST REQUESTS'],
    description=""
)

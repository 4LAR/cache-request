from fastapi import APIRouter
from .ping import *
from .test import *

router = APIRouter()

router.add_api_route(
    "/ping",
    ping,
    methods=['GET'],
    tags=['PING'],
    description="Ping Pong"
)

router.add_api_route(
    "/hello",
    test,
    methods=['GET'],
    tags=['TEST'],
    description="Hello %s"
)

router.add_api_route(
    "/div",
    div,
    methods=['POST'],
    tags=['TEST'],
    description="Hello %s"
)

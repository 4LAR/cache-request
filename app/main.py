from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import *

from globals import *
from routers import *
from cache import *

app = FastAPI()

app.include_router(router, prefix="")

# thread_cache_lifetime()

# test_cache_requests = Cache_requests(
#     based_url = "http://127.0.0.1:8080",
#     timeout = "3",
#     ping_url = "/ping",
# )

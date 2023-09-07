from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import *

from globals import *
from routers import *

app = FastAPI()

app.include_router(router, prefix="")

# thread_cache_lifetime()

import logging
import logging.config
import random
import string
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.apps.auth import admin, auth, users
from src.apps.orders import orders
from src.apps.products import products
from src.db.database import database

from . import settings

app = FastAPI(
    title="Ecommerce Backend Application",
    # description=settings.site_description,
    version="0.0.1",
    openapi_tags=settings.tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/docs"
)


app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(admin.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger('orderLogger')


# event handler for the startup of the application
@app.on_event("startup")
async def startup():
    logging.config.dictConfig(settings.logging_config)
    await database.connect()


# event handler for the shutdown of the application
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


'''
optional middleware to time request processing. 
uncomment out the below function and change FASTAPI_LOG_LEVEL in settings to 'DEBUG' to see these logs / results in console.

@app.middleware("http")
async def log_requests(request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.debug(f"rid={idem} path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.debug(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    return response
'''


@app.get("/", tags=["Home"], summary="Home Page", response_class=HTMLResponse)
async def root(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home.html", context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from core import settings
from .db.database import database
from .auth import admin, auth, users
from .orders import orders
from .products import products


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
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="core/static"), name="static")

templates = Jinja2Templates(directory="core/templates")


# event handler for the startup of the application
@app.on_event("startup")
async def startup():
    await database.connect()


# event handler for the shutdown of the application
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", tags=["Home"], summary="Home Page", response_class=HTMLResponse)
async def root(request: Request, name: str = "to my application"):
    return templates.TemplateResponse("home.html", {"request": request, "name": name})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

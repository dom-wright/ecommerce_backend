from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.db.database import database
from .products import products
from .orders import orders
from .customers import customers, admin


app = FastAPI()


@app.get("/", tags=["Home"], summary="Home Page")
async def root():
    html = "<h1>MY HOME PAGE</h1>"
    return HTMLResponse(html)


app.include_router(orders.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(admin.router)


# event handler for the startup of the application
@app.on_event("startup")
async def startup():
    await database.connect()


# event handler for the shutdown of the application
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

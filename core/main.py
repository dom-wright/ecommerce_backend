from fastapi import FastAPI, status, HTTPException
from enum import Enum
from .routers import customers, products, orders
from core.database import database
from fastapi.responses import HTMLResponse

app = FastAPI()


class Tags(Enum):
    home = "Home"
    customers = "Customers"
    products = "Products"
    orders = "Orders"


@app.get("/", tags=[Tags.home], summary="Home Page")
async def root():
    html = "<h1>MY HOME PAGE</h1>"
    return HTMLResponse(html)


app.include_router(orders.router)
app.include_router(customers.router)
app.include_router(products.router)


# event handler for the startup of the application
@app.on_event("startup")
async def startup():
    await database.connect()


# event handler for the shutdown of the application
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

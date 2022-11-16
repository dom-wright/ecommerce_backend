from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from enum import Enum
from .routers import customers
from core.database import database

app = FastAPI()
app.include_router(customers.router)


class Tags(Enum):
    home = "Home"
    customers = "Customers"
    products = "Products"
    orders = "Orders"


# event handler for the startup of the application
@app.on_event("startup")
async def startup():
    await database.connect()


# event handler for the shutdown of the application
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", tags=[Tags.home], summary="Home Page")
async def root():
    return "MY ROOT PAGE"

from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from enum import Enum
from databases import Database
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String
)
from .routers import customers

app = FastAPI()
app.include_router(customers.router)


class Tags(Enum):
    home = "Home"
    customers = "Customers"
    products = "Products"
    orders = "Orders"


# DATABASES
DATABASE_URL = 'postgresql+asyncpg://localhost:5432/my_orders_db'
database = Database(DATABASE_URL)

metadata = MetaData()
# engine = create_engine(DATABASE_URL)

customers_table = Table(
    "customers",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("address", String),
    Column("email", String)
)


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


@app.get("/database/", status_code=status.HTTP_200_OK)
# response_model=List[CustomerResponse]
async def read_customers():
    query = """SELECT * FROM customers;"""
    rows = await database.fetch_all(query)
    # query = customers_table.select()
    # rows = await database.fetch_all(query=query)
    return rows

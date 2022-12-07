from fastapi import HTTPException
from sqlalchemy import (
    select,
    text,
    distinct
)
from ..db.database import (
    database,
    customers_table as ct
)


async def customer_by_id(id: int):
    query = select(ct).where(ct.c.id == id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID = {id} not found.")
    return record


async def customer_counties():
    query = select(distinct(ct.c.county)).order_by(ct.c.county)
    counties = await database.fetch_all(query)
    if not counties:
        raise HTTPException(
            status_code=404, detail=f"No counties found. Check there are customers in the database.")
    return counties

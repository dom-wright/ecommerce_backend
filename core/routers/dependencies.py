from fastapi import HTTPException
from sqlalchemy import (
    select
)
from ..db.database import (
    database,
    customers_table as ct,
    products_table as pt,
    orders_table as ot
)


async def return_record_by_id(id: int):
    query = select(pt).where(pt.c.id == id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID = {id} not found.")
    return record

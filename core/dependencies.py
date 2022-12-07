from sqlalchemy import (
    insert,
    update
)
from fastapi import HTTPException
from .db.database import (
    database
)


async def create_record(table, values):
    values_dict = values.dict()
    insert_query = insert(table).values(values_dict).returning('*')
    new_record = await database.fetch_one(insert_query)
    if not new_record:
        raise HTTPException(
            status_code=404, detail="Insertion failed.")
    return new_record._mapping


async def update_record(table, record, new_values):
    update_query = update(table).where(table.c.id == record.id).values(
        new_values).returning("*")
    amended_record = await database.fetch_one(update_query)
    return amended_record._mapping

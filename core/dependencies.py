from sqlalchemy import (
    insert,
    update
)
from fastapi import HTTPException
from .db.database import database
from .auth.schemas import UserResponse


def email_user(user: UserResponse, message=""):
    # add logic for sending email to user
    print(f"Message to {user.email}: ", message)


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        # add the meta to the the received message before entering into the log.
        log.write(message)


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

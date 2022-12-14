from fastapi import HTTPException
from sqlalchemy import (
    select,
    distinct
)
from ..db.database import (
    database,
    users_table as ut
)


async def user_counties():
    query = select(distinct(ut.c.county)).order_by(ut.c.county)
    counties = await database.fetch_all(query)
    if not counties:
        raise HTTPException(
            status_code=404, detail=f"No counties found. Check there are users in the database.")
    return counties

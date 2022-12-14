from fastapi import APIRouter, status, HTTPException
from ..db.database import database
from ..auth.schemas import (
    UserResponse
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "User not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse], summary="Get users", description="Returns a list of users", response_description="The list of users.",)
async def users(skip: int = 0, limit: int = 10):
    select_query = f"""SELECT id, username, full_name, email, date_joined, address, county FROM users OFFSET :skip LIMIT :limit;"""
    users = await database.fetch_all(select_query, {'skip': skip, 'limit': limit})
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse, summary="Gets a user", description="Gets a user based on their ID.", response_description="The user.")
async def user_by_id(id: int):
    query = """SELECT  id, username, full_name, email, date_joined, address, county FROM users WHERE id = :id;"""
    user = await database.fetch_one(query, {'id': id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

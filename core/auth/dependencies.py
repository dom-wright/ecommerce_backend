from datetime import datetime, timedelta
from sqlalchemy import select
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core import settings
from ..db.database import (
    database,
    users_table as ut
)
from .utils import verify_password
from .schemas import UserResponse, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# retrieves the user from the database and returns it.
async def get_user(username: str):
    select_user_query = select(ut).where(
        ut.c.username == username)
    user = await database.fetch_one(select_user_query)
    if user:
        return user


# gets the user and then verifies the password against the saved hashed password.
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# creates and returns the JWT token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# accepts JWT token, extracts username, creates a TokenData object with it. then uses the get_user function to retrieve the user.
# the dependency 'oauth2_scheme' extracts and returns the token from the Authorization header as a string, or responds with a 401.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def user_by_id(id: int):
    query = select(ut).where(ut.c.id == id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"User with ID = {id} not found.")
    return record

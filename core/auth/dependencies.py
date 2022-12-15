from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import select, insert, distinct
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .. import settings
from ..db.database import database, users_table as ut
from .utils import verify_password, get_password_hash
from .schemas import UserRegisterRequest, UserResponse, TokenData


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token',
    description='To test, use username="test_user" and password="password", or register an account through /auth/register/'
)


# retrieves user from database and returns it.
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


# creates and returns the JWT token (if user successfully authenticates).
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


# calls get_currrent_user first (above), then checks user is active before returning user to view.
def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# gets user by id.
async def get_user_by_id(id: int):
    query = select(ut).where(ut.c.id == id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"User with ID = {id} not found.")
    return record


async def create_user(user: UserRegisterRequest):
    user_vals = user.dict()
    hashed_password = get_password_hash(user_vals["password1"])
    del user_vals["password1"]
    del user_vals["password2"]
    user_vals["hashed_password"] = hashed_password
    insert_query = insert(ut).values(user_vals).returning('*')
    user = await database.fetch_one(insert_query)
    return user


async def user_counties():
    query = select(distinct(ut.c.county)).order_by(ut.c.county)
    counties = await database.fetch_all(query)
    if not counties:
        raise HTTPException(
            status_code=404, detail=f"No counties found. Check there are users in the database.")
    return counties

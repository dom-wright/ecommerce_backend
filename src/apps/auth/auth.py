from datetime import timedelta
from fastapi import (
    APIRouter,
    BackgroundTasks,
    status,
    HTTPException,
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm
from src import settings
from src.db import database
from src.dependencies import email_user
from .schemas import Token, UserResponse
from .dependencies import (
    authenticate_user,
    get_current_active_user,
    create_access_token,
    create_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# register user.
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(background_tasks: BackgroundTasks, user: create_user = Depends()):
    background_tasks.add_task(
        email_user, user, message="Welcome to the site!")
    return user._mapping


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user

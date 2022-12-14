from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# checks form password matches hash in database.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# used for creating the password hash when creating a new account.
def get_password_hash(password):
    return pwd_context.hash(password)

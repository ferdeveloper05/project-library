import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from models.auth_model import Token, TokenData, User, UserInDB

router = APIRouter(
    prefix="/authen",
    tags=["Autenticacion"]
)

load_dotenv()

#openssl rand -hex 32 para generar la key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


DB_USERS = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "is_active": True,
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
    }
}

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_shema = OAuth2PasswordBearer('authen/token')

def verify_password(plain_password, hashed_password): 
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password): 
    return password_hash.hash(password)

def get_user(database, username: str): 
    if username in database: 
        user_dict = database[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str): 
    user = get_user(fake_db, username)
    if not user: 
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password): 
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None): 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_shema)]): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError: 
        raise credentials_exception
    user = get_user(DB_USERS, token_data.username)
    if user is None: 
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token: 
    user = authenticate_user(DB_USERS, form_data.username, form_data.password)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta= access_token_expire)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User: 
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]) -> list[dict]: 
    return [{"item_id": "Foo", "owner": current_user.username}]
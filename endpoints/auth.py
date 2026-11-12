from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.auth_model import Token, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

router = APIRouter(
    prefix='/example/auth',
    tags=['Authentication']
)

DB_USERS = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "email": "user1@gmail.com", 
        "hashed_password": "hola1234"
    },
    "user2": {
        "username": "user2",
        "full_name": "User Two",
        "email": "user2@gmail.com",
        "hashed_password": "hashed_password_2"
    }
}

@router.get('/', tags=['Authentication'])
async def auth_root():
    return {'message': 'Authentication endpoint'}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # For demonstration purposes, we are using a simple comparison.
    # In a real application, you should use a proper hashing algorithm like bcrypt.
    return plain_password == hashed_password

def encode_token(data: dict):
    # For demonstration purposes, using a simple payload and secret key
    token = jwt.encode(data, "your_secret_key", algorithm="HS256")
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )

def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    user_data = DB_USERS.get(username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return User(**user_data)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return get_user(token)

@router.post('/token', tags=['Authentication'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = DB_USERS.get(form_data.username)
    
    #if not user or user['hashed_password'] != form_data.password:
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    # Generate a JWT token (for demonstration purposes, using a simple payload)
    token_payload = {
        "sub": user['username'],
        "email": user['email'], 
        "password": user['hashed_password']
    }
    token = encode_token(token_payload)
    
    return Token(access_token=token, token_type="bearer")

@router.get('/me', response_model=User, tags=['Authentication'])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
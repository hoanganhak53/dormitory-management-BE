import os
import jwt
from fastapi import Depends, HTTPException, status, Header
from beanie import PydanticObjectId
from app.models.user import UserData
from fastapi.security import OAuth2PasswordBearer
class PermissionDeniedException(Exception):
    pass

os.environ["JWT_SECRET_KEY"] = "78DBDE372E7932A18B891BB69D118"
os.environ["JWT_ALGORITHM"] = "HS256"

default_secret_key = os.getenv('JWT_SECRET_KEY')
default_algorithm = os.getenv('JWT_ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def require_user(token: str= Depends(oauth2_scheme)):
    try:
        data = decode_token(token)
        return data.get("user_id")
    except Exception as e:
        error = e.__class__.__name__
        print(error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')


def generate_token(
    payload=None, secret_key=default_secret_key,
    algorithm=default_algorithm,
):
    payload = payload or {}
    access_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm
    )
    if isinstance(access_token, str):
        return access_token
    else :
        return access_token.decode('utf-8')


def decode_token(
    encoded_token, leeway=0, secret_key=default_secret_key,
    algorithm=default_algorithm
):
    try:
        data = jwt.decode(
            encoded_token, secret_key,
            algorithms=[algorithm], leeway=leeway
        )
        return data
    except jwt:
        raise PermissionDeniedException(
            'Signature expired. Please log in again.'
        )
    except jwt.InvalidTokenError:
        raise PermissionDeniedException('Invalid token. Please log in again.')
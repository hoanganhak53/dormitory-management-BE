import os
import jwt


class PermissionDeniedException(Exception):
    pass


default_secret_key = os.getenv('JWT_SECRET_KEY')
default_algorithm = os.getenv('JWT_ALGORITHM')


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
    except jwt.ExpiredSignatureError:
        raise PermissionDeniedException(
            'Signature expired. Please log in again.'
        )
    except jwt.InvalidTokenError:
        raise PermissionDeniedException('Invalid token. Please log in again.')
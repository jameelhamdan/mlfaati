import jwt
import base64
from jwt import exceptions as jwt_exceptions
from datetime import datetime, timedelta
from django.conf import settings

JWT_ALGORITHM = 'HS256'

__all__ = ['encode_token', 'verify_token', 'jwt_exceptions']


def encode_token(data: dict, exp_in: 'timedelta' = None, secret_key: str = settings.SECRET_KEY) -> str:
    """
    Function to encode data into JWT token
    :param data: Data to be encoded
    :param exp_in: timedelta for token to expire on
    :param secret_key: secret key to be used
    :return: token
    """
    if exp_in:
        data.update({
            'exp': datetime.utcnow() + exp_in
        })

    return str(base64.b64encode(jwt.encode(data, secret_key, JWT_ALGORITHM).encode('utf-8')), 'utf-8')


def verify_token(token: str, secret_key: str = settings.SECRET_KEY) -> dict:
    """
    Function to verify and decode the token generate in _encode_token_ function,
    will raise PyJWTError if the token didn't verify correctly
    :param token: token to be decoded
    :param secret_key: secret key the token was generated with
    :return: token data
    """
    try:
        token = base64.b64decode(token).decode('utf-8')
    except Exception as e:
        raise jwt_exceptions.DecodeError from e
    # Must be encoded with same secret key defined in settings
    return jwt.decode(token, secret_key, leeway=timedelta(seconds=5), algorithms=[JWT_ALGORITHM, ])

"""JWT token manager module."""

from datetime import datetime, timedelta
from jose import JWTError, jwt


class JwtTokenManager:
    """JWT token manager"""

    ALGORITHM = 'HS256'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        """Created JWT token with passed data."""

        expire = datetime.utcnow() + expires_delta

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.ALGORITHM)

        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        """Decodes given token and returns decoded data."""

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.ALGORITHM])
        except JWTError:
            payload = {}

        return payload


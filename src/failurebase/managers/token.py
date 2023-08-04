from datetime import datetime, timedelta
from jose import JWTError, jwt


class JwtTokenManager:

    ALGORITHM = 'HS256'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_access_token(self, data: dict, expires_delta: timedelta | None = timedelta(minutes=15)):

        if expires_delta is None:
            expires_delta = timedelta(expires_delta)

        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_sub(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.ALGORITHM])
        except JWTError:
            return
        else:
            return payload.get("sub")


from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class CredentialsSchema(BaseModel):
    uid: str
    secret: str

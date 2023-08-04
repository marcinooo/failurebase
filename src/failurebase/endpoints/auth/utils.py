"""Authentication utils."""

from typing import Annotated
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from dependency_injector.wiring import inject, Provide

from ...services.client import ClientService
from ...services.api_key import ApiKeyService
from ...managers.token import JwtTokenManager
from ...managers.secret import SecretManager
from ...containers import Application
from ...schemas.client import GetClientSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_key_scheme = APIKeyHeader(name="Api-Key", auto_error=False)


@inject
def get_current_client(

    token: Annotated[str, Depends(oauth2_scheme)],

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    jwt_manager: JwtTokenManager = Depends(Provide[Application.managers.jwt_manager])

) -> GetClientSchema:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    uid = jwt_manager.get_sub(token)
    if uid is None:
        raise credentials_exception

    client = client_service.get_one_by_uid(uid=uid)
    if client is None:
        raise credentials_exception

    return client


@inject
def get_api_key(

    api_key: str = Security(api_key_scheme),

    api_key_service: ApiKeyService = Depends(Provide[Application.services.api_key_service]),

    secret_manager: SecretManager = Depends(Provide[Application.managers.secret_manager])

) -> str:

    paginated_api_keys = api_key_service.get_all()

    api_keys = [secret_manager.decrypt(item.encrypted_value) for item in paginated_api_keys.items]
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API KEY",
            headers={"Api-Key": "API KEY"},
        )

    return api_key

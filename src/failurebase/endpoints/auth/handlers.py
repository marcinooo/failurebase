from datetime import timedelta
from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from ...services.client import ClientService
from ...managers.token import JwtTokenManager
from ...managers.secret import SecretManager
from ...containers import Application
from ...schemas.auth import Token, CredentialsSchema


router = APIRouter()


@router.post(
    '/token',
    responses={
        200: {'model': Token, 'description': 'Access token'}
    }
)
@inject
def login_for_access_token(

    credentials: CredentialsSchema,

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    secret_manager: SecretManager = Depends(Provide[Application.managers.secret_manager]),

    jwt_manager: JwtTokenManager = Depends(Provide[Application.managers.jwt_manager]),

    access_token_expire_minutes: int = Depends(Provide[Application.config.EVENTS_PER_PAGE])

) -> Response:
    client = client_service.get_one_by_uid(uid=credentials.uid)

    if not client or not secret_manager.verify_hash(credentials.secret, client.secret.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client UID or secret",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = jwt_manager.create_access_token(
        data={"sub": client.uid}, expires_delta=access_token_expires
    )

    token = Token(access_token=access_token, token_type="bearer")
    json_compatible_content = jsonable_encoder(token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)

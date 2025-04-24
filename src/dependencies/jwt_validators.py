from typing import Annotated
from abc import ABCMeta, abstractmethod
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from src.exceptions.auth_exceptions import (
    InvalidTokenException,
    InvalidAccessTokenException,
    InvalidRefreshTokenException,
    UnauthenticatedException,
)
from src.token_blacklist.main import check_revoked_token
from src.utils.tokens.auth_token import decode_auth_token


class TokenBearer(HTTPBearer, metaclass=ABCMeta):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        try:
            creds = await super().__call__(request)
        except:
            raise UnauthenticatedException()

        payload = decode_auth_token(creds.credentials)
        if payload is None or not self.validate_token(payload):
            raise InvalidTokenException()
        self.verify_token(payload)

        return payload

    def validate_token(self, token_data: dict) -> bool:
        return not check_revoked_token(token_data["jti"])

    @abstractmethod
    def verify_token(self, token_data: dict) -> None: ...


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if token_data["type"] != "access":
            raise InvalidAccessTokenException()


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if not token_data["type"] != "refresh":
            raise InvalidRefreshTokenException()


AccessTokenValidator = Annotated[dict, Depends(AccessTokenBearer())]
RefreshTokenValidator = Annotated[dict, Depends(RefreshTokenBearer())]

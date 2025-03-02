from fastapi import status, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from datetime import datetime, timezone
from abc import ABCMeta, abstractmethod
from typing import Annotated
from utils import SingletonPattern
from .utils import decode_token


class TokenBearer(SingletonPattern, HTTPBearer, metaclass=ABCMeta):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)

        token_data = decode_token(creds.credentials)
        if token_data is None or not self.validate_token(token_data):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "Invalid or expired credentials"
            )
        self.verify_token(token_data)

        return token_data

    def validate_token(self, token_data: dict) -> bool:
        expiry_timestamp = datetime.fromtimestamp(token_data["exp"], timezone.utc)
        if expiry_timestamp < datetime.now(timezone.utc):
            return False
        return True

    @abstractmethod
    def verify_token(self, token_data: dict) -> None: ...


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if token_data["refresh"]:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if not token_data["refresh"]:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Please provide a refresh token",
            )


AccessTokenRequired = Annotated[dict, Depends(AccessTokenBearer())]
RefreshTokenRequired = Annotated[dict, Depends(RefreshTokenBearer())]

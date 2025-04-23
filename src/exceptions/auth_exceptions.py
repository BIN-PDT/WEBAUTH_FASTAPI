from fastapi import status
from .base_exception import BaseException


class InvalidLoginCredentialsException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {"message": "Invalid username or password."}


class InvalidTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {"message": "Invalid or expired token."}


class InvalidAccessTokenException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"message": "Invalid access token."}


class InvalidRefreshTokenException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"message": "Invalid refresh token."}


class InsufficientPermissionException(BaseException()):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"message": "User are not allowed to perform this action."}


class UnauthenticatedException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {"message": "User is not authenticated."}

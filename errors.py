from fastapi import status


class BaseError(Exception):
    status_code: int
    detail: dict


class UsernameAlreadyExistsError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "User with username already exists"}


class EmailAlreadyExistsError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "User with email already exists"}


class InvalidCredentialsError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {"message": "Invalid username or password"}


class InvalidTokenError(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {"message": "Invalid or expired credentials"}


class AccessTokenRequiredError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"messsage": "Please provide an access token"}


class RefreshTokenRequiredError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"messsage": "Please provide an refresh token"}


class InsufficientPermissionError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {"message": "You are not allowed to perform this action"}


class UserNotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = {"message": "User not found"}

from fastapi import status
from .base_exception import BaseException


class DuplicateUsernameException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "User with username already in use."}


class DuplicateEmailException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "User with email already in use."}


class VerifiedEmailException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "Email is verified."}


class WrongPasswordException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = {"message": "Wrong password."}


class UserNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = {"message": "User not found."}


class ConfirmPasswordMismatchException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {"message": "Confirm password mismatches new password."}

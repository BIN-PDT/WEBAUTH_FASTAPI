from fastapi import FastAPI, Request
from src.exceptions.base_exception import BaseException
from src.schemas.api_response import APIResponse


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseException)
    def handle_base_exception(_: Request, exc: BaseException):
        return APIResponse(status_code=exc.status_code, **exc.detail).send()

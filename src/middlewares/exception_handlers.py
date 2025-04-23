from fastapi import FastAPI, Request
from exceptions.base_exception import BaseException
from schemas.api_response import APIResponse


async def base_exception_handler(_: Request, exc: BaseException):
    return APIResponse(status_code=exc.status_code, **exc.detail).send()


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(BaseException, base_exception_handler)

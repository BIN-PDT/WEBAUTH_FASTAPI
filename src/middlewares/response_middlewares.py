from fastapi import FastAPI, Request
from src.schemas.api_response import APIResponse


def add_response_middlewares(app: FastAPI):
    @app.middleware("http")
    async def handle_api_response(request: Request, call_next):
        response = await call_next(request)
        return response.send() if isinstance(response, APIResponse) else response

from typing import Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel


class APIResponse(SQLModel):
    status_code: int
    message: str | None = None
    data: Any = None
    errors: Any = None

    def send(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder(self),
        )

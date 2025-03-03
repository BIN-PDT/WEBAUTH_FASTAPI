from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from errors import BaseError
from auth.routes import router


app = FastAPI()
app.include_router(router, prefix="/auth", tags=["auth"])


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

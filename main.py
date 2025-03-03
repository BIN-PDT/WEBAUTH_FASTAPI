from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from errors import BaseError
from auth.routes import router


app = FastAPI()
app.include_router(router, prefix="/auth", tags=["auth"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=("*",),
    allow_methods=("*",),
    allow_headers=("*",),
    allow_credentials=True,
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=("*",),
    www_redirect=True,
)


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

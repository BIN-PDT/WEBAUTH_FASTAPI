from fastapi import FastAPI
from src.routes.index import router
from src.middlewares.exception_handlers import add_exception_handlers
from src.middlewares.security_middlewares import add_security_middlewares
from src.middlewares.response_middlewares import add_response_middlewares


app = FastAPI()
app.include_router(router)

add_exception_handlers(app)
add_security_middlewares(app)
add_response_middlewares(app)

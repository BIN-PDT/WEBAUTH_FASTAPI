from fastapi import FastAPI
from routes.index import router
from middlewares.security import add_security_middleware
from middlewares.exception_handlers import add_exception_handlers


app = FastAPI()
app.include_router(router)

add_security_middleware(app)
add_exception_handlers(app)

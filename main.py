from fastapi import FastAPI
from auth.routes import router


app = FastAPI()
app.include_router(router, prefix="/auth", tags=["auth"])

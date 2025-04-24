from fastapi import APIRouter
from src.routes.auth import router as authRouter


router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["auth"])

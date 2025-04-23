from fastapi import APIRouter
from .auth import router as authRouter


router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["auth"])

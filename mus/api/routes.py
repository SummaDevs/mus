from fastapi import APIRouter

from mus.api.modules.system.routes import router as system_router

api_router = APIRouter()

api_router.include_router(system_router, tags=["System"])

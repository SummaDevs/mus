from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from mus.api.config.config import api_config
from mus.api.response.schema import DefaultResponse
from mus.core.db.deps import get_db

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=DefaultResponse)
def root() -> dict:
    return {
        "status": True,
        "msg": "Project information",
        "details": {
            "name": f"{api_config['PROJECT_NAME']}",
            "version": f"{api_config['APP_VERSION']}",
        },
    }


@router.get("/health", status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_health(db: AsyncSession = Depends(get_db)) -> dict:
    try:
        healthy = await db.execute(text("SELECT 1"))
        if healthy.scalars().first() is None:
            raise HTTPException(
                status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                detail={"msg": "Not Healthy"}
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"status": True, "msg": "Healthy"}

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from shopping.api.metadata import API_DESCRIPTION, API_TITLE, API_VERSION


class HealthcheckDTO(BaseModel):
    title: str
    description: str
    version: str
    start_date: datetime
    uptime: float = None


HEALTH_INFO = HealthcheckDTO(
    title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION, start_date=datetime.utcnow()
)

router = APIRouter(tags=["api"])


@router.get("/healthcheck", response_model=HealthcheckDTO)
async def healthcheck():
    result = HEALTH_INFO.copy()
    result.uptime = (datetime.utcnow() - HEALTH_INFO.start_date).total_seconds()
    return result

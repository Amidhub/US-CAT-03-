from fastapi import HTTPException, Depends, Header
from src.core.config import settings


async def verify_service_key(x_service_key: str = Header(...)) -> str:
    """Проверка X-Service-Key для B2C доступа"""
    if x_service_key != settings.service_key:
        raise HTTPException(status_code=403, detail="Invalid service key")
    return x_service_key
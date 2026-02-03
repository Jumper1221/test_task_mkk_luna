from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.core.config import settings

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def validate_api_key(x_api_key: str = Security(api_key_header)) -> str:
    if not x_api_key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="API ключ отсутствует",
        )

    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Недействительный API ключ",
        )

    return x_api_key

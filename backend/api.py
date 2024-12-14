from fastapi import APIRouter, status

from .metadata import Config


api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
def api_root():
    return {
        "apiname": Config.API_NAME,
        "version": Config.API_VERSION
    }

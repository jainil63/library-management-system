from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api import api_router
from .metadata import Config


# API
app = FastAPI(
    title=Config.APP_NAME,
    summary=Config.APP_SUMMARY,
    description=Config.APP_DESCRIPTION,
    version=Config.API_VERSION,
    license_info=Config.LICENSE_INFO
)


# Serving the static files using middleware
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


# Redirecting user to frontend
@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, tags=["Frontend"])
def root():
    return RedirectResponse("/frontend")


# Health Check
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health():
    return {
        "message": "Server is up in running!!",
        "api-home": "/api/v1",
        "version": "0.1.0",
        "status": "running!!!"
    }


# API Router
app.include_router(api_router, prefix="/api/v1", tags=["Backend"])

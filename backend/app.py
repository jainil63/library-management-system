from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api import api_router


# API
app = FastAPI(
    title="LIBIFY API",
    summary="library management system",
    description="LIBIFY is a comprehensive library management system designed to assist library administrators in efficiently managing their libraries. The system ensures ease of use, secure data handling, and a robust platform for both users and administrators.",
    version="v1",
    license_info={ 
        "name": "MIT", 
        "identifier": "MIT", 
        "url": "https://github.com/jainil63/library-management-system/blob/main/LICENSE.txt"
    }, 
)


# Serving the static files using middleware
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


# Redirecting user to frontend
@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def root():
    return RedirectResponse("/frontend")


# Health Check
@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "message": "Server is up in running!!",
        "api-home": "/api/v1",
        "version": "0.1.0",
        "status": "running!!!"
    }


# API Router
app.include_router(api_router, prefix="/api/v1", tags=["api"])

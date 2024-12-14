from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from .api import api_router
from .metadata import Config
from .custom_schema import modify_openapi_schema


app = FastAPI(
    title=Config.APP_NAME,
    version=Config.API_VERSION,
    summary=Config.APP_SUMMARY,
    description=Config.APP_DESCRIPTION,
    license_info=Config.LICENSE_INFO
)


# Ref:- https://fastapi.tiangolo.com/how-to/extending-openapi/#overriding-the-defaults
def custom_openapi_schema_generator():
    # return cached openapi schema
    if app.openapi_schema:
        return app.openapi_schema
    
    # call the fastapi defualt method
    openapi_schema = get_openapi(
        title=Config.APP_NAME,
        version=Config.API_VERSION,
        summary=Config.APP_SUMMARY,
        description=Config.APP_DESCRIPTION,
        routes=app.routes
    )
    
    modify_openapi_schema(openapi_schema) # function modify openapi_schema itself to have custom property
    
    app.openapi_schema = openapi_schema # cacheing
    return app.openapi_schema

app.openapi = custom_openapi_schema_generator  # Modify fastapi schema function with custom function


app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, tags=["Frontend"])
def root():
    return RedirectResponse("/frontend")


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health():
    return {
        "message": "Server is up in running!!",
        "api-home": "/api/v1",
        "version": "0.1.0",
        "status": "running!!!"
    }


app.include_router(api_router, prefix="/api/v1", tags=["Backend"])

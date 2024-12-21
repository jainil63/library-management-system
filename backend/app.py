from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from . import database
from .metadata import Config
from .custom_schema import modify_openapi_schema
from .utils import verify_and_decode_token


app = FastAPI(
    title=Config.APP_NAME,
    version=Config.API_VERSION,
    summary=Config.APP_SUMMARY,
    description=Config.APP_DESCRIPTION,
    license_info=Config.LICENSE_INFO
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    database.init_db()
    database.ensure_admin_user()
    print("INFO:     Database initialized!!!")


@app.middleware("http")
async def get_user_middleware(request: Request, call_next):
    token = request.cookies.get("access-token")
    
    if not token:
        request.state.user = None
    
    if token:
        user = verify_and_decode_token(token)
        if user:
            request.state.user = user
        else:
            request.state.user = None
    
    print(request.state.user)
    response = await call_next(request)
    return response


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


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    return "Server is up in running!! 👍👍"


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, tags=["Frontend"])
def root():
    return RedirectResponse("/frontend")


@app.get("/reset/{masterpassword}", tags=["Super Admins Only"])
def reset_all_data(masterpassword: str):
    """
    It reset all the database.
    """
    if masterpassword == Config.MASTERPASSWORD:
        database.delete_db()
        database.init_db()
        database.ensure_admin_user()
        print("INFO:     Database reinitialized!!!")
        return RedirectResponse("/frontend")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect MasterPassword!!")


app.include_router(api_router, prefix="/api/v1", tags=["Backend"])

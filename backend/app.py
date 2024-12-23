from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from . import database
from .metadata import Config
from .utils import verify_and_decode_token


app = FastAPI(
    title=Config.APP_NAME,
    version=Config.API_VERSION,
    summary=Config.APP_SUMMARY,
    description=Config.APP_DESCRIPTION,
    license_info=Config.LICENSE_INFO,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect MasterPassword!!",
        )


app.include_router(api_router, prefix="/api/v1", tags=["Backend"])

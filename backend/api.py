import sqlite3

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from .metadata import Config
from .routers.userrouter import user_router
from .routers.bookrouter import book_router
from .routers.authrouter import auth_router
from .utils import verify_and_decode_token
from .database import get_db

api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
def api_root():
    return {
        "apiname": Config.API_NAME,
        "version": Config.API_VERSION
    }


@api_router.get("/profile", status_code=status.HTTP_200_OK)
def user_profile(request: Request):
    token = request.cookies.get("access-token")
    
    response = RedirectResponse(url="/frontend/loginpage.html", status_code=status.HTTP_303_SEE_OTHER)
    
    if not token:
        return response
    
    payload = verify_and_decode_token(token)
    if payload == False:
        response.delete_cookie("access-token")
        return response
    
    return { "token": token, "user": payload }


@api_router.get("/borrows")
def get_all_active_borrow_book(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE borrowby IS NOT NULL")
    borrow = cursor.fetchall()
    return borrow


api_router.include_router(user_router, prefix="/users", tags=["Backend", "Users"])
api_router.include_router(book_router, prefix="/books", tags=["Backend", "Books"])
api_router.include_router(auth_router, prefix="/auth", tags=["Backend", "Auth"])

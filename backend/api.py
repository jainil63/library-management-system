import sqlite3

from fastapi import APIRouter, Depends, status

from .metadata import Config
from .routers.userrouter import user_router
from .routers.bookrouter import book_router
from .routers.authrouter import auth_router
from .database import get_db

api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
def api_root():
    return {"apiname": Config.API_NAME, "version": Config.API_VERSION}


@api_router.get("/borrows")
def get_all_active_borrow_book(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE borrowby IS NOT NULL")
    borrow = cursor.fetchall()
    return borrow


api_router.include_router(user_router, prefix="/users", tags=["Backend", "Users"])
api_router.include_router(book_router, prefix="/books", tags=["Backend", "Books"])
api_router.include_router(auth_router, prefix="/auth", tags=["Backend", "Auth"])

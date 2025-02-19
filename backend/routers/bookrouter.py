import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status

from ..database import get_db
from ..schemas import BookIn, BookOut, BorrowParams


book_router = APIRouter()


@book_router.get("/")
def get_books(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return books


@book_router.post("/borrow")
def borrow_book(
    params: Annotated[BorrowParams, Query()],
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    cursor = conn.cursor()

    cursor.execute("SELECT username FROM user WHERE id = ?", (params.userid,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found!!"
        )

    cursor.execute("SELECT borrowby FROM books WHERE id = ?", (params.bookid,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found!!"
        )

    if book["borrowby"] is None:
        cursor.execute(
            "UPDATE books SET borrowby = ? WHERE id = ?", (params.userid, params.bookid)
        )
        conn.commit()
        return {"message": "successfully", "success": True}
    else:
        return {
            "message": "failure, book is not avaliable to borrow!!",
            "success": False,
        }


@book_router.post("/return")
def return_book(
    params: Annotated[BorrowParams, Query()],
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET borrowby = NULL WHERE id = ? AND borrowby = ?",
        (params.bookid, params.userid),
    )
    conn.commit()

    cursor.execute("SELECT borrowby FROM books WHERE id = ?", (params.bookid,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found!!"
        )

    if book["borrowby"] == params.userid:
        return {"message": "success", "success": True}
    else:
        return {"message": "failure, some error occured!!", "success": False}


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookOut)
def create_book(
    book: BookIn, request: Request, conn: sqlite3.Connection = Depends(get_db)
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    if book.title == "" or book.desc == "" or book.author == "" or book.category == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Data provided is not valid!!",
        )

    if book.price < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Negative prize is not allowed!!",
        )

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, desc, author, category, price) VALUES (?, ?, ?, ?, ?)",
        (book.title, book.desc, book.author, book.category, book.price),
    )
    conn.commit()
    book_id = cursor.lastrowid
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    newbook = cursor.fetchone()
    return dict(newbook)


@book_router.put("/{id}", response_model=BookOut)
def update_book_by_id(
    id: int, book: BookIn, request: Request, conn: sqlite3.Connection = Depends(get_db)
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    if book.title == "" or book.desc == "" or book.author == "" or book.category == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Data provided is not valid!!",
        )

    if book.price < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Negative prize is not allowed!!",
        )

    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE books 
            SET title = ?, desc = ?, author = ?, category = ?, price = ?
            WHERE id = ?
        """,
        (book.title, book.desc, book.author, book.category, book.price, id),
    )
    conn.commit()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    updateuser = cursor.fetchone()
    if updateuser:
        return dict(updateuser)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found!!!"
        )


@book_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(
    id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

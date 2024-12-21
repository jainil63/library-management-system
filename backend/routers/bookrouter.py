import sqlite3
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

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
def borrow_book(params: Annotated[BorrowParams, Query()],  conn: sqlite3.Connection = Depends(get_db)):
    return NotImplementedError()


@book_router.post("/return")
def return_book(params: Annotated[BorrowParams, Query()],  conn: sqlite3.Connection = Depends(get_db)):
    return NotImplementedError()


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookOut)
def create_user(book: BookIn, conn: sqlite3.Connection = Depends(get_db)):
    if book.title == "" or book.desc == "" or book.author == "" or book.category == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Data provided is not valid!!")
    
    if book.price < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Negative prize is not allowed!!")
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, desc, author, category, price) VALUES (?, ?, ?, ?, ?)",
    )
    conn.commit()
    book_id = cursor.lastrowid
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    newbook = cursor.fetchone()
    return dict(newbook)


@book_router.put("/{id}", response_model=BookOut)
def update_book_by_id(id: int, book: BookIn, conn: sqlite3.Connection = Depends(get_db)):
    if book.title == "" or book.desc == "" or book.author == "" or book.category == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Data provided is not valid!!")
    
    if book.price < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Negative prize is not allowed!!")
        
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE books 
            SET title = ?, desc = ?, author = ?, category = ?, price = ?
            WHERE id = ?
        """, (book.title, book.desc, book.author, book.category, book.price, id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    updateuser = cursor.fetchone()
    if updateuser:
        return dict(updateuser)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found!!!")


@book_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

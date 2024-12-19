from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Annotated

from ..database import get_db
from ..models import User

import sqlite3


user_router = APIRouter()


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)",
            (user.fullname, user.username, user.password)
        )
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    newuser = cursor.fetchall()
    return newuser


@user_router.get("/")
def get_users(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users


@user_router.get("/{id}")
def get_user_by_id(id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username Not Found!!!")
    


@user_router.put("/{id}")
def update_user_by_id(id: int, user: User, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE users 
            SET username = ?, password = ?, email = ?, mobileno = ?
            WHERE id = ?
        """, (user.username, user.password, user.email, user.mobileno, id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    updateuser = cursor.fetchone()
    if updateuser:
        return updateuser
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username Not Found!!!")


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

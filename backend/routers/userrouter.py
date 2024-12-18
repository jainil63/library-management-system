from fastapi import APIRouter, Depends, HTTPException, status
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
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password)
        )
        user_id = cursor.lastrowid

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    newuser = cursor.fetchall()
    print(newuser)
    
    return newuser


@user_router.get("/")
def get_users(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
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

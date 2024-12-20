import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse

from ..database import get_db
from ..utils import create_token
from ..schemas import LoginFormData, CreateAccountFormData, Token


auth_router = APIRouter()


@auth_router.post("/login")
def login(data: Annotated[LoginFormData, Form()], conn: sqlite3.Connection = Depends(get_db)):
    if data.username == "" or data.password == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Data provided is not valid!!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, isadmin FROM users WHERE username = ?", (data.username,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!!!")
    
    user = dict(user)
    password = user["password"]
    
    if not data.password == password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!!")
    
    token = create_token(id=str(user["id"]), username=user["username"], isadmin=user["isadmin"])
    response = RedirectResponse(url="/frontend", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access-token", value=token)
    return response


@auth_router.get("/logout")
def logout():
    response = RedirectResponse(url="/frontend", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access-token")
    return response


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: Annotated[CreateAccountFormData, Form()], conn: sqlite3.Connection = Depends(get_db)):
    if data.fullname == "" or data.email == "" or data.username == "" or data.password == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENITITY, detail="Data provided is not valid!!!")
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (fullname, email, username, password) VALUES (?, ?, ?, ?)",
            (data.fullname, data.email, data.username, data.password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!!!")
    
    user_id = cursor.lastrowid
    cursor.execute("SELECT id, username, isadmin FROM users WHERE id = ?", (user_id,))
    newuser = cursor.fetchone()
    
    token = create_token(id=str(newuser["id"]), username=newuser["username"], isadmin=newuser["isadmin"])
    response = RedirectResponse(url="/frontend", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access-token", value=token)
    return response

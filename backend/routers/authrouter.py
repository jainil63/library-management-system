import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel

from ..database import get_db
from ..utils import create_token

class LoginFormData(BaseModel):
    username: str
    password: str


class CreateAccountFormData(BaseModel):
    fullname: str
    email: str
    username: str
    password: str


auth_router = APIRouter()


@auth_router.post("/login")
@auth_router.post("/signup")
def signup(data: Annotated[CreateAccountFormData, Form()]):
    raise NotImplementedError()
def login(data: Annotated[LoginFormData, Form()], conn: sqlite3.Connection = Depends(get_db)):
    if data.username == "" or data.password == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="data provided is not valid!!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, isadmin FROM users WHERE username = ?", (data.username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found!!!")
    
    user = dict(user)
    password = user["password"]
    
    if not data.password == password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password!!")
    
    token = create_token(id=str(user["id"]), username=user["username"], isadmin=user["isadmin"])
    return { "message": "login in successfully!!", "token": token}

    

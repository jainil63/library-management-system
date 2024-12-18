from fastapi import APIRouter, Depends, status
from typing import Annotated

from ..database import Database
from ..models import User


user_router = APIRouter()


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    db = Database.get_db()
    db.execute_sql("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR, password VARCHAR)")
    return 200


@user_router.get("/")
def get_users():
    db = Database.get_db()
    result = db.execute_sql("SELECT * FROM users");
    return result

@user_router.get("/{id}")
def get_user_by_id(id: int):
    raise NotImplementedError()

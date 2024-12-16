from fastapi import APIRouter


from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional

from ..database import data


class User(BaseModel):
    id: Optional[int] = -1
    username: str
    password: str


user_router = APIRouter()


@user_router.post("/")
def create_user(user: User):
    user.id = len(data["users"])
    data["users"].append(user)
    return user


@user_router.get("/")
def get_users():
    return data["users"]


@user_router.get("/{id}")
def get_user_by_id(id: int):
    return data["users"][id]

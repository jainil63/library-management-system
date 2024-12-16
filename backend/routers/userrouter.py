from fastapi import APIRouter, status

from ..database import Database
from ..models import User


user_router = APIRouter()


@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    user.id = len(Database.data["users"])
    Database.data["users"].append(user.model_dump())
    return user


@user_router.get("/")
def get_users():
    users = Database.data["users"]
    return {
        "users": users
    }


@user_router.get("/{id}", response_model=User)
def get_user_by_id(id: int):
    return Database.data["users"][id]

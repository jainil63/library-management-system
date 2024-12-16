from fastapi import APIRouter, status

from ..models import User


auth_router = APIRouter()


@auth_router.get("/login")
def login():
    raise NotImplementedError()


@auth_router.post("/signup")
def signup():
    raise NotImplementedError()

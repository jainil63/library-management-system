from fastapi import APIRouter, status, Form
from pydantic import BaseModel

from typing import Annotated


class LoginFormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


class CreateAccountFormData(BaseModel):
    full name: str
    email: str
    username: str
    password: str
    model_config = {"extra": "forbid"}


auth_router = APIRouter()


@auth_router.get("/login")
def login(data: Annotated[LoginFormData, Form()]):
    raise NotImplementedError()


@auth_router.post("/signup")
def signup(data: Annotated[CreateAccountFormData, Form()]):
    raise NotImplementedError()

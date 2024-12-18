from fastapi import APIRouter, status, Form
from pydantic import BaseModel

from typing import Annotated


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
def login(data: Annotated[LoginFormData, Form()]):
    raise NotImplementedError()


@auth_router.post("/signup")
def signup(data: Annotated[CreateAccountFormData, Form()]):
    raise NotImplementedError()

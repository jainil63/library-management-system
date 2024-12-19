from pydantic import BaseModel

from typing import Optional


class User(BaseModel):
    id: Optional[int | None] = None
    fullname: str
    email: str
    username: str
    password: str
    mobileno: str
    isadmin: bool

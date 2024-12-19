from pydantic import BaseModel


# Auth Forms
# -----------------------------------------


class LoginFormData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
    message: str = "Loggedin Successfully!!"


class CreateAccountFormData(BaseModel):
    fullname: str
    email: str
    username: str
    password: str


# Users
# -----------------------------------------

class UserIn(BaseModel):
    fullname: str
    email: str
    username: str
    password: str
    mobileno: str
    isadmin: bool = False


class UserOut(BaseModel):
    id: int
    fullname: str
    email: str
    username: str
    mobileno: str
    isadmin: bool


# Books
# -----------------------------------------


class BookBase(BaseModel):
    pass
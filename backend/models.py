class UserBase:
    id: Optional[int | None] = None
    fullname: str
    email: str
    username: str
    password: str
    mobileno: str
    isadmin: bool = False

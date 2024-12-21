import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from ..database import get_db
from ..schemas import UserIn, UserOut


user_router = APIRouter()


@user_router.get("/")
def get_users(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, conn: sqlite3.Connection = Depends(get_db)):
    if (
        user.fullname == ""
        or user.email == ""
        or user.username == ""
        or user.password == ""
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Data provided is not valid!!",
        )

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (fullname, email, username, password) VALUES (?, ?, ?, ?)",
            (user.fullname, user.email, user.username, user.password),
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!!!"
        )

    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    newuser = cursor.fetchone()
    return dict(newuser)


@user_router.get("/profile")
def get_user_profile(request: Request, conn: sqlite3.Connection = Depends(get_db)):
    if not request.state.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not login!!"
        )

    id = request.state.user["id"]
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()

    if user:
        user = dict(user)
        cursor.execute("SELECT * FROM books WHERE borrowby = ?", (id,))
        borrowbooks = cursor.fetchall()
        if borrowbooks:
            user["books"] = borrowbooks
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username Not Found!!!"
        )


@user_router.put("/", response_model=UserOut)
def update_user(
    user: UserIn, request: Request, conn: sqlite3.Connection = Depends(get_db)
):
    if not request.state.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not login!!"
        )

    id = request.state.user["id"]
    if (
        user.fullname == ""
        or user.email == ""
        or user.username == ""
        or user.password == ""
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Data provided is not valid!!",
        )

    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users 
            SET username = ?, password = ?, email = ?, mobileno = ?
            WHERE id = ?
        """,
        (user.username, user.password, user.email, user.mobileno, id),
    )
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    updateuser = cursor.fetchone()
    if updateuser:
        return dict(updateuser)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username Not Found!!!"
        )


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
    id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
):
    if not request.state.user or request.state.user["isadmin"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Only Route!!"
        )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

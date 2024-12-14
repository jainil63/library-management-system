from fastapi import APIRouter


api_router = APIRouter()


@api_router.get("/")
def api_homepage():
    return {
        "apiname": "LIBIFY API - Library Management System",
        "version": "0.1.0"
    }

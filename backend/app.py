from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="LIBIFY API",
    description="Library Management System",
    version="0.1.0",
    license_info={ "name": "MIT", "identifier": "MIT"}
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def root():
    return RedirectResponse("/frontend/index.html")


@app.get("/api/v1")
def api_homepage():
    return {
        "apiname": "LIBIFY API - Library Management System",
        "version": "0.1.0",
        "homepage": "/index.html",
        "documentation": "/docs"
    }

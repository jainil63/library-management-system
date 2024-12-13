from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="./frontend"), name="frontend")

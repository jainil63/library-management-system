import json
from pathlib import Path


def get_frontend_paths(path):
    with open(path) as file:
         return json.load(file)


def get_sqlscript_content(path):
    sql = ""
    with open(path) as file:
        sql = file.read()
    # print(sql.replace("\n", ""))
    return sql


class Config:
    APP_NAME = "LIBIFY APP"
    APP_SUMMARY = "Library Management System"
    APP_DESCRIPTION = """LIBIFY is a comprehensive library management system designed to assist library administrators in efficiently managing their libraries. The system ensures ease of use, secure data handling, and a robust platform for both users and administrators."""
    APP_VERSION = "0.1.0"
    API_NAME = "LIBIFY API - Library Management System"
    API_VERSION = "v1"
    LICENSE_INFO = {
        "name": "MIT LICENSE", 
        "identifier": "MIT", 
        "url": "https://github.com/jainil63/library-management-system/blob/main/LICENSE.txt"
    }
    FRONTEND_PATH = get_frontend_paths(Path(__file__).parent / ".." / "frontend" / "frontend_paths.json")
    INIT_DB_SQL = get_sqlscript_content(Path(__file__).parent / "initdb.sql")
    DATABASE_URL = "app.db"
    ADMIN_USER = {
        "fullname": "monster",
        "username": "admin",
        "password": "beastuser",
        "email": "monster@admin.com"
    }

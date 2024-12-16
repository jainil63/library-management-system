import os
import json


class Database:
    filepath = "database.json"
    data = {
        "users": []
    }
    
    def load():
        if not os.path.exists(Database.filepath):
            print("APP LOGS: Database not exists!!!!")
            return
        
        with open(Database.filepath) as file:
            Database.data = json.load(file)
    
    def save():
        with open(Database.filepath, "w") as file:
            json.dump(Database.data, file, indent=4)

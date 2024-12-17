import sqlite3


class Database:
    instance = None
    
    @staticmethod
    def get_db(name = ":memory:"):
        if not Database.instance:
            Database.instance = Database(name)
        return Database.instance
    
    @staticmethod
    def close():
        Database.instance.disconnect()
        Database.instance = None
    
    def __init__(self, name: str):
        self.name = name
        self.conn = None
        self.cursor = None
        self.isactive = False
    
    def connect(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.isactive = True
        print("Successfully connected with database!!!")
        return self
    
    def execute_sql(self, sqlstatement, *args):
        if not self.isactive:
            raise Exception("Database is not connected!!")
        
        self.cursor.execute(sqlstatement, *args)
        self.cursor.commit()
        return self.cursor.fetchall()

    def disconnect(self):
        self.isactive = False
        self.cursor.close()
        self.conn.close()
        print("Successfully disconnected with database!!!")
    

import sqlite3


from .metadata import Config


class Database:
    instance = None
    
    @staticmethod
    def init(name = ":memory:"):
        db = Database(name)
        db.connect()
        db.cursor.executescript(Config.INIT_DB_SQL)
        Database.instance = db
    
    @staticmethod
    def get_db():
        if not Database.instance.isactive:
            Database.instance.connect()
        return Database.instance
    
    @staticmethod
    def close():
        Database.instance.disconnect()
    
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
        self.conn.commit()
        return self.cursor.fetchall()

    def disconnect(self):
        self.isactive = False
        self.cursor.close()
        self.conn.close()
        print("Successfully disconnected with database!!!")


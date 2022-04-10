import sqlite3
DATABASE_NAME = "drones.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS drone(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT CHECK( LENGTH(serial_number) <= 100 ) NOT NULL,
                model TEXT CHECK( model IN ('Lightweight','Middleweight','Cruiserweight','Heavyweight')) NOT NULL DEFAULT 'Lightweight',
				weight_limit REAL NOT NULL,
				battery_capacity REAL NOT NULL,
                state TEXT CHECK( state IN ('IDLE','LOADING','LOADED','DELIVERING', 'DELIVERED', 'RETURNING')) NOT NULL DEFAULT 'IDLE'
            )
            """,
            """CREATE TABLE IF NOT EXISTS medication(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
				weight REAL NOT NULL,
				code TEXT NOT NULL,
                image BLOB NOT NULL,
                drone_id INTEGER NOT NULL
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
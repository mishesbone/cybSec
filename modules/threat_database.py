import sqlite3

class ThreatDatabase:
    def __init__(self, db_name="threats.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            hash TEXT,
            behavior TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_threat(self, name, hash_val, behavior):
        query = "INSERT INTO threats (name, hash, behavior) VALUES (?, ?, ?)"
        self.conn.execute(query, (name, hash_val, behavior))
        self.conn.commit()

    def fetch_all_threats(self):
        query = "SELECT * FROM threats"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

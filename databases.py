import sqlite3

from settings import DB_FILE


class Database:
    def __init__(self):
        self._conn = sqlite3.connect(DB_FILE, isolation_level=None)
        self._cur = self._conn.cursor()

    def execute(self, query, params):
        return self._cur.execute(query, params)

    def __del__(self):
        self._conn.close()

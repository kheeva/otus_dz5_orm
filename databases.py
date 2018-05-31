import sqlite3
from settings import DB_FILE


class Database:
    conn = None

    def db_connect(func):
        def decorated(*args, **kwargs):
            try:
                conn = sqlite3.connect(DB_FILE)
                cur = conn.cursor()
            except Exception as e:
                result = e.args
            else:
                try:
                    result = func(cur, *args, **kwargs)
                except Exception as e2:
                    print(e2)
                    result = e2.args
                else:
                    conn.commit()
                finally:
                    # cur.close()
                    # conn.close()
                    pass
            return result
        return decorated

    @db_connect
    def execute(cur, query, *args):
        cur.execute(query, args)
        return cur

    def __del__(self):
        if self.conn and self.conn.open:
            self.conn.close()

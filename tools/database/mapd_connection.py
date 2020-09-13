from tools.database.connection import Connection, Cursor
import pymapd


class MapdConnection(Connection):
    def __init__(self, host, name, user, password):
        self.connection = pymapd.connect(user=user, password=password, host=host, dbname=name)

    def _make_cursor(self):
        return MapdCursor(self.connection.cursor())


class MapdCursor(Cursor):
    def __init__(self, cursor: pymapd.Cursor):
        self.c = cursor

    def fetch(self, count: int=1):
        if count == 1:
            return self.c.fetchone()
        elif count > 1:
            return self.c.fetchmany(count)
        elif count == -1:
            return self.c.fetchall()

    def execute(self, sql: str) -> None:
        self.c.execute(sql)

    def close(self):
        self.c.close()

import os

from tools.database.mapd_connection import MapdConnection
from tools.config import Config
from layers.data import table

GUIDE = \
"""
SQL MANAGER

What would you like to do?
[T]able

[S]cripts
"""


def script(conn):
    name = input("What is the script name?\n")

    with open("scripts/" + name + ".sql", "r") as f:
        sql = f.read()

    print(sql)

    with conn.transact() as c:
        c.execute(sql)
        return False


def main(conn):
    print(GUIDE)
    res = input().lower()

    os.system("clear")
    if res == "t":
        while table.main(conn):
            pass
        return True

    if res == "s":
        while script(conn):
            pass
        return True

    return False


if __name__ == '__main__':
    config = Config("config.json.ini", "Dev")

    conn = MapdConnection(
        config.get_str("database_server"),
        config.get_str("database_name"),
        config.get_str('database_user'),
        config.get_str('database_password'),
    )

    while main(conn):
        pass

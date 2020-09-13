
GUIDE = \
"""

TABLES

[A]dd a new table

OR select the table ID that you want to edit
"""


def main(conn):
    print(GUIDE)

    tables = conn.connection.get_tables()
    for name, i in zip(tables, range(0, len(tables))):
        print("[{: <3}] {}".format(i, name))

    res = input().lower()

    if res == "a":
        add(conn)
        return True

    if res.isnumeric():
        res = tables[int(res)]

        while edit_single(conn, res):
            pass

        return True

    return False


def edit_single(conn, table):

    table_details = conn.connection.get_table_details(table)

    print("TABLE: " + table)
    print()
    for col in table_details:
        print("{: <24}{: <12}\t{}".format(col.name, col.type, "TRUE" if col.nullable else "FALSE"))
    print()

    print("[D]elete table")
    res = input().lower()

    if res == "d":
        delete(conn, table)
        return False

    return False


def delete(conn, table):
    with conn.transact() as c:
        c.execute("DROP TABLE {}".format(table))


def add(conn):
    name = input("Name?\n")

    with conn.transact() as c:
        c.execute("CREATE TABLE {} (y INTEGER);".format(name))

import sqlite3
import config


def open_con():
    con = sqlite3.connect(config.db_name)  # create db file and open connection
    cur = con.cursor()  # create cursor
    return con, cur


def close_con(con):
    con.close()


def print_from_table(cur, table_name):
    cur.execute("SELECT * FROM {table_name}".format(table_name=table_name))
    headers = list(map(lambda attr: attr[0], cur.description))
    results = [{header: row[i] for i, header in enumerate(headers)} for row in cur]
    for r in results:
        print(r)

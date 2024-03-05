from collections import defaultdict
from dataclasses import dataclass
import sqliteDB
import config


@dataclass
class BakeryItemType:
    item_type_id: int
    item_type_category: str
    item_type_name: str
    bakeryItemTypes = defaultdict(list)

    def __init__(self, item_type_category: str, item_type_name: str):
        self.item_type_category = item_type_category
        self.item_type_name = item_type_name


def get_bakery_item_types(print_types: bool):
    con, cur = sqliteDB.open_con()
    cur.execute("SELECT * FROM {table}".format(table=config.bakeryItemTypeTableName))
    sql_res = cur.fetchall()
    sqliteDB.close_con(con)
    if print_types:
        for i in sql_res:
            print(i)
    return sql_res


def create_bakery_item_type_table():  # Supposed to operate once
    table_name = config.bakeryItemTypeTableName
    con, cur = sqliteDB.open_con()
    res = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'".format(table_name=table_name))
    res_sql_query = res.fetchone()
    sql_query = """CREATE TABLE {table_name}
    ([ID] INTEGER PRIMARY KEY,category, type, UNIQUE (category, type))""".format(
        table_name=table_name)
    if not res_sql_query:
        cur.execute(sql_query)  # create table BakeryItemType
        con.commit()
        print(table_name, "table created")
    elif table_name not in res_sql_query:
        cur.execute(sql_query)  # create table BakeryItemType
        con.commit()
        print(table_name, "table created")
    else:
        print(table_name, "table was not created, it already exists")  # print to verify that the table has been created
    sqliteDB.close_con(con)


def init_bakery_item_type_list():  # only for testing
    bakery_item_type_list = BakeryItemType
    bakery_item_type_list.bakeryItemTypes["Dry"].append("Cookies")
    bakery_item_type_list.bakeryItemTypes["Dry"].append("English cake")
    bakery_item_type_list.bakeryItemTypes["Cold"].append("English cake")
    bakery_item_type_list.bakeryItemTypes["Cold"].append("Birthday cake")
    bakery_item_type_list.bakeryItemTypes["Cold"].append("19 Diameter")
    bakery_item_type_list.bakeryItemTypes["Cold"].append("24 Diameter")
    bakery_item_type_list.bakeryItemTypes["Cold"].append("28 Diameter")
    # show categories
    for k in bakery_item_type_list.bakeryItemTypes.keys():
        print(k, ":")
        for v in bakery_item_type_list.bakeryItemTypes[k]:
            print(" " * 5, v)
    return bakery_item_type_list


def insert_bakery_item_type_table_by_list(bakery_item_type_list):
    con, cur = sqliteDB.open_con()
    for k in bakery_item_type_list.bakeryItemTypes.keys():
        for v in bakery_item_type_list.bakeryItemTypes[k]:
            sql_query = """SELECT * FROM {table_name} 
            ORDER BY ID DESC LIMIT 1""".format(table_name=config.bakeryItemTypeTableName)
            res = cur.execute(sql_query)
            if not res.fetchone():
                type_id = 1
            else:
                res = cur.execute(sql_query)
                type_id = res.fetchone()[0] + 1
            try:
                cur.execute("""INSERT INTO {table_name} 
                            VALUES ({type_id},'{k}','{v}')""".format(
                    type_id=type_id, k=k, v=v,
                    table_name=config.bakeryItemTypeTableName))
                con.commit()
            except Exception as ex:
                str_to_search = "UNIQUE constraint"
                if str_to_search in ex.args[0]:
                    print(str_to_search, ": '{k}','{v}'".format(k=k, v=v), "\tcontinue to next iteration")
                    continue
                else:
                    raise ex
    sqliteDB.close_con(con)

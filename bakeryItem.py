from dataclasses import dataclass
import numpy as np
import pandas as pd
from pydantic import validate_call
import bakeryItemType
import config
import sqliteDB


@validate_call
@dataclass
class BakeryItem:
    item_id: int
    item_type_key: int
    item_name: str
    price: float  # NIS
    item_des: str

    def __init__(self, item_name: str, price: float, item_des: str):
        self.item_id = 0
        self.item_type_key = 0
        self.item_name = item_name
        self.price = price
        # self.prDate=prDate
        # self.expDate=expDate
        self.item_des = item_des

        input_types = bakeryItemType.get_bakery_item_types()
        num = np.array(input_types)
        reshaped = num.reshape(7, 3)
        print("BakeryItem created, now choose item category from the table bellow:\n",
              pd.DataFrame(reshaped, columns=['Key', 'Category', 'SubCategory']))
        self.itemTypeKey = int(
            input("enter key"))  # need to put inside a while loop - continue until correct input from user
        con, cur = sqliteDB.open_con()
        res = cur.execute("SELECT ID FROM BakeryItemType")
        if self.itemTypeKey not in list(sum(res.fetchall(), ())):
            raise "key is not valid"
        else:
            print("BakeryItem created")
        sqliteDB.close_con(con)

    def update_bakery_item_type(self, item_type: int):
        print("update_bakery_item_type")
        self.item_type_key = item_type

    def insert_bakery_item(self):
        con, cur = sqliteDB.open_con()
        try:
            cur.execute("""INSERT INTO {table_name} VALUES (
                      {item_id},
                      {item_type_key},
                      '{item_name}',
                      {price},
                      '{item_des}')""".format(
                item_id='Null',
                item_type_key=self.item_type_key,
                item_name=self.item_name,
                price=self.price,
                item_des=self.item_des,
                table_name=config.bakeryItemTableName))
        except Exception as ex:
            str_to_search = "UNIQUE constraint"
            if str_to_search in ex.args[0]:
                print("Error inserting bakeryItem, ", str_to_search,
                      ": {{'{item_type_key}','{item_name}','{price}','{item_des}}}'".format(
                          item_type_key=self.item_type_key,
                          item_name=self.item_name,
                          price=self.price,
                          item_des=self.item_des),
                      "\nItem name already belong to the chosen category, please choose different.")
            else:
                raise ex
        con.commit(con)
        sqliteDB.close_con(con)


def get_bakery_items_head_inc():
    con, cur = sqliteDB.open_con()
    cur.execute("SELECT * FROM {table_name}".format(table_name=config.bakeryItemTableName))
    headers = list(map(lambda attr: attr[0], cur.description))
    results = [{header: row[i] for i, header in enumerate(headers)} for row in cur]
    sqliteDB.close_con(con)
    return results


def get_bakery_items(print_types: bool):
    con, cur = sqliteDB.open_con()
    res = cur.execute("SELECT * FROM {table_name}".format(table_name=config.bakeryItemTableName))
    sql_res = res.fetchall()
    sqliteDB.close_con(con)
    if print_types:
        for r in sql_res:
            print(r)
    return sql_res


def init_bakery_items_list():  # for testing
    bakery_item_list = [
        {'item_id': '0', 'item_type_key': 1, 'item_name': 'Butter cookies', 'price': '8', 'item_des': 'Large box'},
        {'item_id': '0', 'item_type_key': 1, 'item_name': 'Oatmeal cookies', 'price': '15', 'item_des': 'Large box'},
        {'item_id': '0', 'item_type_key': 2, 'item_name': 'Carrot cake', 'price': '44',
         'item_des': 'Carrot cake with sugar frosting'},
        {'item_id': '0', 'item_type_key': 3, 'item_name': 'Cheese cake', 'price': '55',
         'item_des': 'Cheese cake with crumbles'},
        {'item_id': '0', 'item_type_key': 4, 'item_name': 'Chocolate cake', 'price': '140',
         'item_des': 'Chocolate cake with sprinkles'},
        {'item_id': '0', 'item_type_key': 5, 'item_name': 'Tricolad', 'price': '120',
         'item_des': 'Chocolate cake with three types of chocolate - white, milk and dark'}]
    for item in bakery_item_list:
        print(item)
    return bakery_item_list


def create_bakery_item_table():  # use one time when starting a project
    table_name = config.bakeryItemTableName
    con, cur = sqliteDB.open_con()
    res = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'".format(table_name=table_name))
    res_sql_query = res.fetchone()
    sql_query = ("""
    CREATE TABLE {table_name}(
    [item_id] INTEGER PRIMARY KEY,item_type_key INTEGER, 
    item_name, price,item_des, UNIQUE (item_type_key, item_name))
    """.format(table_name=table_name))
    if not res_sql_query:
        cur.execute(sql_query)
        print(table_name, "table created")
    elif table_name not in res_sql_query:
        cur.execute(sql_query)
        print(table_name, "table created")
    else:
        print(table_name, "table was not created, it already exists")
    sqliteDB.close_con(con)


def init_bakery_item_table(bakery_item_list: list):
    error_count = 0
    con, cur = sqliteDB.open_con()
    for item in bakery_item_list:
        sql_query = """SELECT * FROM {table_name} 
                    ORDER BY item_id DESC LIMIT 1
                    """.format(table_name=config.bakeryItemTableName)
        res = cur.execute(sql_query)
        if not res.fetchone():
            item_id = 1
        else:
            res = cur.execute(sql_query)
            item_id = res.fetchone()[0] + 1
        try:
            cur.execute("""INSERT INTO {table_name} VALUES (
                          {item_id},
                          {item_type_key},
                          '{item_name}',
                          {price},
                          '{item_des}')""".format(
                item_id=item_id,
                item_type_key=item.get('item_type_key'),
                item_name=item.get('item_name'),
                price=item.get('price'),
                item_des=item.get('item_des'),
                table_name=config.bakeryItemTableName))
            con.commit()
        except Exception as ex:
            str_to_search = "UNIQUE constraint"
            if str_to_search in ex.args[0]:
                print(str_to_search, ": {item_id},{item_type_key},'{item_name}',{price},'{item_des}'".format(
                    item_id=item.get('item_id'),
                    item_type_key=item.get('item_type_key'),
                    item_name=item.get('item_name'),
                    price=item.get('price'),
                    item_des=item.get('item_des')),
                      "\tcontinue to next iteration")
                error_count += 1
                continue
            else:
                raise ex

    sqliteDB.close_con(con)
    if error_count == 0:
        print("""All items inserted to '{table_name}' table\n"
              "Number of rows inserted: '{inserted}'
              """.format(
                table_name=config.bakeryItemTableName,
                inserted=len(bakery_item_list)))
    else:
        print("""Not all items inserted to '{table_name}'' table\n"
              "Number of rows inserted: '{inserted}'\n
              Number of rows not inserted: '{not_inserted}'""".format(
                table_name=config.bakeryItemTableName,
                inserted=len(bakery_item_list) - error_count,
                not_inserted=error_count))

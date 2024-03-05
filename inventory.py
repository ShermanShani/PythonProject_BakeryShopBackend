from dataclasses import dataclass
from datetime import date, timedelta
import bakeryItem
import config
import sqliteDB
import numpy as np
import pandas as pd


# need to continue checking why the validate arguments decor is not working when loading 'BakeryItem' class instance
# into 'Inventory' class
@dataclass
class Inventory:
    product_id: int
    bakery_item: bakeryItem
    pr_date: date
    good_for_days: int  # amount of days for stock
    stock: int  # amount of product for stock

    def __init__(self, pr_date: date, stock: int, good_for_days: int):
        self.product_id = 0
        self.pr_date = pr_date
        self.stock = stock
        self.good_for_days = good_for_days

    # def insert_inventory(self):
    #     con, cur = sqlCon.open_con()
    #     try:
    #         cur.execute("""INSERT INTO {table_name} VALUES (
    #                     {item_id},
    #                     {item_type_key},
    #                     '{item_name}',
    #                     {price},
    #                     '{item_des}')""".format(
    #             item_id='Null',
    #             item_type_key=self.bakery_item.item_type_key,
    #             item_name=self.bakery_item.item_name,
    #             price=self.bakery_item.price,
    #             item_des=self.bakery_item.item_des,
    #             table_name=config.bakeryItemTableName))
    #         con.commit()
    #     except Exception as ex:
    #         str_to_search = "UNIQUE constraint"
    #         if str_to_search in ex.args[0]:
    #             print("""Error inserting bakeryItem, ",str_to_search,":
    #                 {{'{item_type_key}','{item_name}','{price}','{item_des}}}'""".format(
    #                 item_type_key=self.bakery_item.item_type_key,
    #                 item_name=self.bakery_item.item_name,
    #                 price=self.bakery_item.price,
    #                 item_des=self.bakery_item.item_des), """\n"
    #                                         "Item name already belong to the chosen category,
    #                                         please choose again.""")
    #         else:
    #             sqlCon.close_con(con)
    #             raise ex
    #     sqlCon.close_con(con)


def init_inventory_list(bakery_item_list: list, inventory_list: list, stock: int, stock_inc: int,
                        good_for_days_inc: int, days_timedelta: int, good_for_days: int):
    pr_date = date.today() - timedelta(days=days_timedelta)
    print("len(bakery_items_list): ", len(bakery_item_list))
    for item in bakery_item_list:
        inventory_list.append(
            {'product_id': "",
             'item_id': item['item_id'],
             'pr_date': pr_date,
             'stock': stock,
             'exp_date': date.today() + timedelta(days=good_for_days)
             })
        stock += stock_inc
        good_for_days += good_for_days_inc
    return inventory_list


def create_inventory_table():
    table_name = config.inventoryTableName
    con, cur = sqliteDB.open_con()
    res = cur.execute("""SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='{table_name}'
                    """.format(table_name=table_name))
    res_sql_query = res.fetchone()
    sql_query = """CREATE TABLE {table_name}
                ([product_id] INTEGER PRIMARY KEY, item_id, pr_date, stock,exp_date, UNIQUE (item_id, pr_date))
                """.format(table_name=table_name)
    if not res_sql_query:
        cur.execute(sql_query)
        print(table_name, "table created")
    elif table_name not in res_sql_query:
        cur.execute(sql_query)
        print(table_name, "table created")
    else:
        print(table_name, "table was not created, it already exists")


def init_inventory_table(inventory_list: list):
    table_name = config.inventoryTableName
    error_count = 0
    con, cur = sqliteDB.open_con()
    for item in inventory_list:
        try:
            cur.execute("""INSERT INTO {table_name} VALUES (
                        {product_id}, {item_id}, '{pr_date}',
                        {stock}, '{exp_date}')""".format(
                product_id='Null', item_id=item.get('item_id'),
                pr_date=item.get('pr_date'), stock=item.get('stock'),
                exp_date=item.get('exp_date'), table_name=table_name))
        except Exception as ex:
            str_to_search = "UNIQUE constraint"
            if str_to_search in ex.args[0]:
                print(str_to_search, ": {item_id},{pr_date},'{stock}',{exp_date}".format(
                    item_id=item.get('item_id'), pr_date=item.get('pr_date'),
                    stock=item.get('stock'), exp_date=item.get('exp_date')),
                      "\tcontinue to next iteration")
                error_count += 1
                continue
            else:
                raise ex
    con.commit()
    if error_count == 0:
        print("""All items inserted to '{table_name}' table\n
        Number of rows inserted: '{inserted}'""".format(
            table_name=table_name, inserted=len(inventory_list)))
    else:
        print("""Not all items inserted to '{table_name}'' table\n
                Number of rows inserted: '{inserted}'\n
                Number of rows not inserted: '{not_inserted}'""".format(
                table_name=table_name, inserted=len(inventory_list) - error_count, not_inserted=error_count))


def get_short_exp_inventory_json(days_for_exp, stock_min, stock_max):
    cur, headers, con = get_short_exp_inventory(days_for_exp, stock_min, stock_max)
    results = [{header: row[i] for i, header in enumerate(headers)} for row in cur]
    for r in results:
        print(r)
    sqliteDB.close_con(con)
    return results


def get_short_exp_inventory_table(days_for_exp, stock_min, stock_max):
    cur, headers, con = get_short_exp_inventory(days_for_exp, stock_min, stock_max)
    res = cur.fetchall()
    results_arr = np.array(res)
    reshaped = results_arr.reshape(len(results_arr), len(headers))
    results = pd.DataFrame(reshaped, columns=[headers[0], headers[1], headers[2], headers[3], headers[4]])
    sqliteDB.close_con(con)
    return results


def get_short_exp_inventory(days_for_exp, stock_min, stock_max):
    table_name = config.inventoryTableName
    date_for_exp_max = date.today() + timedelta(days=days_for_exp)
    date_for_exp_min = date.today()
    con, cur = sqliteDB.open_con()
    cur.execute("""SELECT * FROM '{table_name}'
                WHERE expDate BETWEEN '{date_for_exp_min}' AND '{date_for_exp_max}' 
                AND stock BETWEEN {stock_min} AND {stock_max}""".format(
                table_name=table_name,
                date_for_exp_min=date_for_exp_min,
                date_for_exp_max=date_for_exp_max,
                stock_min=stock_min,
                stock_max=stock_max))
    headers = list(map(lambda attr: attr[0], cur.description))
    return cur, headers, con

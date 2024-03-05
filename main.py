import bakeryItem
import bakeryItemType
import config
import inventory


if config.running_env.lower() == "test":
    # bakeryItemType - init
    bakeryItemType.create_bakery_item_type_table()
    bakery_item_type_list = bakeryItemType.init_bakery_item_type_list()
    bakeryItemType.insert_bakery_item_type_table_by_list(bakery_item_type_list)
    bakeryItemType.get_bakery_item_types(False)
    # bakeryItem - init
    bakeryItem.create_bakery_item_table()
    bakery_item_list = bakeryItem.init_bakery_items_list()
    bakeryItem.init_bakery_item_table(bakery_item_list)
    bakeryItem.get_bakery_items(False)
    # inventory - init
    inventory.create_inventory_table()
    bakery_item_list = bakeryItem.get_bakery_items_head_inc()
    inventory_list = []
    inventory_list = inventory.init_inventory_list(
        inventory_list=inventory_list, bakery_item_list=bakery_item_list,
        stock_inc=5, stock=4, good_for_days_inc=1, good_for_days=30, days_timedelta=1)
    inventory_list = inventory.init_inventory_list(
        inventory_list=inventory_list, bakery_item_list=bakery_item_list,
        stock_inc=3, stock=2, good_for_days_inc=1, good_for_days=20, days_timedelta=5)
    inventory_list = inventory.init_inventory_list(
        inventory_list=inventory_list, bakery_item_list=bakery_item_list,
        stock_inc=3, stock=1, good_for_days_inc=3, good_for_days=3, days_timedelta=9)
    inventory.init_inventory_table(inventory_list)

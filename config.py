running_env = "test"
bakeryItemTypeTableName = "BakeryItemType"
bakeryItemTableName = "BakeryItem"
inventoryTableName = "Inventory"
db_name = "MyBakery.db"
if running_env.lower() == "test":
    good_for_days = 30  # use as default days for all products - on production, should be dynamic


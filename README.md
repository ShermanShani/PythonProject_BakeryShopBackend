Bakery inventory information system - BackEnd - Python based


Background

This application was built for managing a bakery shop inventory, it will be used by the shop staff.
The main objective of using this system is to manage the inventory of the bakery.
The system includes relevant classes for maintaining products category, products of the bakery, inventory and methods for reports/Charts building for analizing the work efficiency. 
Reports functions are generic so they can be triggered by schedueler or manually (need some minor adjustments).


Entities by Class:

1) BakeryItemType - represent category

2) BakeryItem - represent specific item

3) Inventory - represent store stock inventory

*The app doesn't support user interface (yet ;) ) and focusing only on the python backend.


important functions

Class Methods:
1) getBakeryItemTypes()

2) creating new BakeryItem - using init function of Class

3) updatebakeryItemType()

4) getBakeryItems()

5) getBakeryItemsHeadInc() - including headers

6) insertBakeryItem()

7) creating new Inventory - using init function of Class

8) insertInventory()

General methods:
1) printFromTable()

2) getShortExpInventoryJson()

3) getShortExpInventoryTable()

4) getInventoryTableHeaders()

5) getInventoryIncludeNamesTable()

6) getInventoryStockByCategory()

*examples of using methods in the notebook below

from accounts import *
from menus import *
import pandas as pd

# TODO: Transfer all functions into list class
# TODO: Migrate files into separate list.py file?

class Store:
    def __init__(self):
        self.storeid = 0
        self.storename = ""
        self.address = ""
    # def displayStoreDetails():

class Item:
    def __init__(self):
        self.itemid = 0
        self.itemname = ""
        self.price = 0.00
        self.unit = ""
        self.category = ""
        self.productSize = ""
        self.storeid = 0
    # def displayItem():

def storeLookup(cursor, Store):
    # ---------- QUERY store ----------
    try:
        storeName = input("Enter the name of the store: ")
        storeName += "%"
        query = f"SELECT storeid, storename, address FROM stores WHERE storename LIKE '{storeName}' ORDER BY storename ASC"
        cursor.execute(query)

        # Give option to select inventory
        # --- 
        storeResults = cursor.fetchall()
        unpack = storeResults[0]
    except IndexError:
        print("\n\n\nERROR: Store not found")
        lookupMethod = createListMenu()
    else:
        selection = True
        (storeid, storename, address) = unpack

        # Store object
        Store.storeid = storeid
        Store.storename = storename
        Store.address = address
    return selection

def itemLookup(cursor, Item):
    try:
        itemName = input("Enter the name of the item: ")
        itemName += "%"

        # JOIN query
        # --- 

        query = f"SELECT itemid, itemname, price, unit, productSize, storeid FROM items WHERE itemname LIKE '{itemName}' ORDER BY itemname ASC"
        cursor.execute(query)
        itemResults = cursor.fetchall()
        unpack = itemResults[0]
    except IndexError:
        print("ERROR: Item not found")
        lookupMethod = createListMenu()
    else:
        # TODO: Return all objects not just one
        # Enumerate query results?

        selection = True
        (itemid, itemname, price, unit, productSize, storeid) = unpack

        # TODO: User selects which item
        # --- 

        # ---------- Append Item object ---------- 
        Item.itemid = itemid
        Item.itemname = itemname
        Item.price = price
        Item.unit = unit
        Item.productSize = productSize
        Item.storeid = storeid
    return selection

def addAnotherItem():
    addItem = input("Would you like to search for another item? [y/n]: ")
    if (addItem == "y") or (addItem == "Y"):
        userSelection = False
    else:
        userSelection = True
    return userSelection

def priceLookup(cursor):
    """ If grocery item is in the 'database', print the price of the item """
    lookup = False
    while lookup == False:
        try:
            itemName = input("Enter the name of the item: ")
            itemName += "%"

            # JOIN query
            # --- 

            query = f"SELECT itemid, itemname, price, unit, productSize, storeid FROM items WHERE itemname LIKE '{itemName}' ORDER BY itemname ASC"
            cursor.execute(query)
        except IndexError:
            print("ERROR: Item not found")
        else:
            # TODO: Return all objects not just one
            # Enumerate query results?

            itemResults = cursor.fetchall()
            unpack = itemResults[0]
            (itemid, itemname, price, unit, productSize, storeid) = unpack

            # ---------- Append Item object ---------- 
            Item.itemid = itemid
            Item.itemname = itemname
            Item.price = price
            Item.unit = unit
            Item.productSize = productSize
            Item.storeid = storeid

            print("\nResults: \n")
            print(f'{Item.itemid} ---' + " " + Item.itemname + " @ " + str(Item.price) + " per " + Item.unit + "\n")
            
            # ---------- Lookup another item ----------
            nextItem = input("Would you like to select another item? [y/n]: ")
            
            if (nextItem == "y") or (nextItem == "Y"):
                lookup = False
            elif (nextItem == "n") or (nextItem == "N"):
                lookup = True


def showAllItems(cursor, Item):
    """ Prints all available items to window from database """
    query = "SELECT * FROM items"
    cursor.execute(query)
    itemResults = cursor.fetchall()

    df = pd.DataFrame(itemResults, columns=['Item ID', 'Item', 'Store ID', 'Category', 'Subcategory', 'Price', 'Unit', 'Size'])    
    df.set_index('Item ID', inplace=True, drop=True)

    print(df) 
from accounts import *
from menus import createListMenu
import pandas as pd

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
        self.subcategory = ""
        self.productSize = ""
        self.storename = ""
        self.storeid = 0
    # def displayItem():

def storeLookup(cursor, Store):
    # ---------- QUERY store ----------
    try:
        storeName = input("Enter the name of the store: ")
        storeName += "%"
        query = "SELECT storeid, storename, address FROM stores WHERE storename LIKE %s ORDER BY storename ASC"
        cursor.execute(query, (storeName,))

        # Give option to select inventory
        # --- 
        storeResults = cursor.fetchall()
        unpack = storeResults[0]
    except IndexError:
        print("\n\n\nERROR: Store not found")
        lookupMethod = createListMenu()
    except mysql.connector.Error as err:
            returnSQLError(err)
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
        itemName = input("Enter the name of an item: ")
        print("\n\n")
        itemName += "%"

        query = "SELECT i.itemid, i.itemname, s.storename, i.price, i.unit, i.productSize FROM items AS i INNER JOIN stores AS s ON i.storeid = s.storeid WHERE i.itemname LIKE %s ORDER BY i.itemname ASC"
        cursor.execute(query, (itemName,))
        itemResults = cursor.fetchall()

    except IndexError:
        print("ERROR: Item not found")
        lookupMethod = createListMenu()
    except mysql.connector.Error as err:
            returnSQLError(err)
    else:
        df = pd.DataFrame(itemResults, columns=['Item ID', 'Item', 'Store ID', 'Price', 'Unit', 'Size'])    
        df.set_index('Item ID', inplace=True, drop=True)
        if df.empty:
            print("\n\nSorry, no item with that name is in our database")
            return False
        else:
            print(df)
            itemSelect = input("\n\nPlease enter the Item ID # of the item you would like to select: ")
            try:
                float(itemSelect)
            except ValueError:
                print("Invalid entry. Please type the number of the Item ID")
                return False
            except IndexError:
                print("ERROR: Item not found")
                lookupMethod = createListMenu()
            else:
                query = "SELECT i.itemid, i.itemname, s.storename, i.price, i.unit, i.category, i.subcategory, i.productSize, i.storeid FROM items AS i INNER JOIN stores AS s ON i.storeid = s.storeid WHERE i.itemid = %s"
                cursor.execute(query, (itemSelect,))
                itemResults = cursor.fetchall()
                unpack = itemResults[0]
                (itemid, itemname, storename, price, unit, category, subcategory, productSize, storeid) = unpack

                #TODO: DRY
                Item.itemid = itemid
                Item.itemname = itemname
                Item.price = price
                Item.unit = unit
                Item.productSize = productSize
                Item.storeid = storeid
                Item.storename = storename
                Item.category = category
                Item.subcategory = subcategory
                return True

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
    while lookup is False:
        try:
            itemName = input("Enter the name of the item: ")
            itemName += "%"

            # JOIN query
            # --- 

            query = "SELECT itemid, itemname, price, unit, productSize, storeid FROM items WHERE itemname LIKE %s ORDER BY itemname ASC"
            cursor.execute(query, (itemName,))
            itemResults = cursor.fetchall()
            unpack = itemResults[0]
        except IndexError:
            print("\nERROR: Item not found\n")
        except mysql.connector.Error as err:
            returnSQLError(err)
        else:
            # TODO: Return all objects not just one
            # Enumerate query results?
            (itemid, itemname, price, unit, productSize, storeid) = unpack

            # ---------- Append Item object ---------- 
            Item.itemid = itemid
            Item.itemname = itemname
            Item.price = price
            Item.unit = unit
            Item.productSize = productSize
            Item.storeid = storeid

            print("\RESULTS: \n")
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
 
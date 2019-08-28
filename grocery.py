from account import *
from menu import *
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
        self.productSize = ""
        self.storeid = 0
    # def displayItem():

class GroceryList:
    def __init__(self):
        self.user = ""
        self.listName = "Grocery List"
        self.total = 0.00
        self.numOfItems = 0
        self.cart = []

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

def createlist(cursor, database, UserAccount, Store, Item):
    """ Creates new list locally and in rdb """
    
    listname = input("Please enter a name for the list: ")
    userList = {}
    dbList = ""
    lookupMethod = createListMenu()
    
    optionSelect = False
    while optionSelect == False:
        if lookupMethod == "1":

            #TODO: GIVE OPTION TO SELECT STORE BY NEIGHBORHOOD, LIST ALL STORES, ETC (query location table instead)

            optionSelect = storeLookup(cursor, Store)

            userSelection = False
            while userSelection == False:
                print("Options: \n")
                storeSelect = input(f'{Store.storeid} ---' + " " + Store.storename + " @ " + Store.address + "\nSelect a store number or type 'None': ")
                
                if storeSelect == "1": # Dummy statement --------------------------------
                    print("Success")
                    userSelection = True
                elif storeSelect == "None":
                    lookupMethod = createListMenu()
                else:
                    print("\nERROR: Invalid selection")

                print("\n\n")

        # ---------- Query Item ----------
        elif lookupMethod == "2":

            userSelection = False
            while userSelection == False:
                optionSelect = itemLookup(cursor, Item)
                print("\nOptions: \n")
                itemSelection = input(f'\n{Item.itemid} ---' + " " + Item.itemname + " @ " + str(Item.price) + " per " + Item.unit + "\nSelect an item to add to your list or type 'None': ")
                
                if itemSelection == "1": # Dummy statement --------------------------------
                    userList[f"{Item.itemname}"] = f"{Item.price} / {Item.unit}"
                    print(f"\n{Item.itemname} successfully added to {listname}!")
                    print(f"\n\nUser list = \n{userList}\n\n")
                    dbList += str(Item.itemid) + ", "

                    userSelection = addAnotherItem()

                elif itemSelection == "None":
                    userSelection = addAnotherItem()

                else:
                    print("\nERROR: Invalid selection")

                print("\n\n")

            # TODO: INTEGRITYERROR:1062 (23000): DUPLICATE ENTRY ' ' FOR KEY 'PRIMARY'
            # TODO: NEED TO ADD LISTID AND MAKE PRIMARY KEY ISNTEAD OF USERID. make userid foreign key
            query = f"INSERT INTO lists (userid, listname, ListOfItemIDs, totalCost) VALUES ({UserAccount.userid}, '{listname}', '{dbList}', 0.00)"
            cursor.execute(query)
            database.commit()
            
            UserAccount.listCount += 1
            query = f"UPDATE accounts SET listcount = ({UserAccount.listCount}) WHERE userid = {UserAccount.userid}"
            cursor.execute(query)
            database.commit()

        else:
            print("\n\nERROR: Invalid option selected. Please type 1 or 2 and then hit enter.")
            lookupMethod = createListMenu()
        

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

    # TODO: Remove index
    # ---

    print(df) 
            
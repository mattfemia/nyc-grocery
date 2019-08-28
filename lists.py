from accounts import *
from menus import *
import pandas as pd


class GroceryList:
    def __init__(self):
        self.userid = 0
        self.listid = 0
        self.listname = ""
        self.items = ""

        
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
                    dbList += str(Item.itemid) + ","

                    userSelection = addAnotherItem()

                elif itemSelection == "None":
                    userSelection = addAnotherItem()

                else:
                    print("\nERROR: Invalid selection")

                print("\n\n")

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

def viewLists(cursor, UserAccount):
    """ Queries all itemids in each user's list and stitches together itemid, itemname, storename, category, 
    price, unit into a formatted structure """

    query = f"SELECT userid, listid, listname, ListOfItemIDs FROM lists WHERE userid = {UserAccount.userid}"
    cursor.execute(query)
    result = cursor.fetchall()

    currentList = GroceryList()
    currentItem = Item()

    #TODO: This is only accounting for a user having one list -- make it so the user selects which list to edit
    
    for entry in result:
        currentList.listid = entry[1]
        currentList.listname = entry[2]
        currentList.items = entry[3]

        df = pd.DataFrame(columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
        for item in currentList.items:
            if (item != ",") and (item != " "):
                
                currentItem.itemid = item
                query = f"SELECT itemid, itemname, storename, category, price, unit FROM items INNER JOIN stores ON items.storeid = stores.storeid WHERE itemid = '{currentItem.itemid}'"
                cursor.execute(query)
                result = cursor.fetchall()
                df2 = pd.DataFrame(result, columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                df = pd.concat([df, df2])

        df.set_index('Item ID', inplace=True, drop=True)

        
        print(f"\n\nList ID = {currentList.listid}\nList name = {currentList.listname} \n{df}")

    # -------- editList function ----------

    edit = input("\n\nWould you like to edit your lists? [y/n]: ")
    if (edit == "y") or (edit == "Y"):
        listSelect = input("Please enter the List ID shown above the list you would like to edit: ")

        query = f"SELECT userid, listid, listname, ListOfItemIDs FROM lists WHERE listid = {listSelect}"
        cursor.execute(query)
        result = cursor.fetchall()

        currentList = GroceryList()
        currentItem = Item()

        currentList.listid = entry[1]
        currentList.listname = entry[2]
        currentList.items = entry[3]

        df = pd.DataFrame(columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
        for item in currentList.items:
            if (item != ",") and (item != " "):
                
                currentItem.itemid = item
                query = f"SELECT itemid, itemname, storename, category, price, unit FROM items INNER JOIN stores ON items.storeid = stores.storeid WHERE itemid = '{currentItem.itemid}'"
                cursor.execute(query)
                result = cursor.fetchall()
                df2 = pd.DataFrame(result, columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                df = pd.concat([df, df2])

        df.set_index('Item ID', inplace=True, drop=True)

        
        print(f"\nList ID = {currentList.listid}\nList name = {currentList.listname} \n{df}")
        
        # ---- EditListMenu Fxn ---- 
        edited = False
        while edited == False:
            print("\n1 --- Drop item from list\n2 --- Change list name\n3 --- Delete list")
            editListMenu = input("Please type in a number from the menu: ")
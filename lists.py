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

def viewLists(cursor, database, UserAccount):
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

        # TODO: Disable user from accessing lists outside of their own (currently can type any list id and retrieve it)

        listSelect = input("Please enter the List ID shown above the list you would like to edit: ")

        query = f"SELECT userid, listid, listname, ListOfItemIDs FROM lists WHERE listid = {listSelect}"
        cursor.execute(query)
        result = cursor.fetchall()

        currentList = GroceryList()
        currentItem = Item()

        for entry in result:
            currentList.listid = entry[1]
            currentList.listname = entry[2]
            currentList.items = entry[3]

        df = pd.DataFrame(columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
        for item in currentList.items:

            # TODO: Fix this conditional to account for numbers with digits > 1 (10, 23, 123). Need to change list item structure
            if (item != ",") and (item != " "):
                
                currentItem.itemid = item
                query = f"SELECT itemid, itemname, storename, category, price, unit FROM items INNER JOIN stores ON items.storeid = stores.storeid WHERE itemid = '{currentItem.itemid}'"
                cursor.execute(query)
                result = cursor.fetchall()
                df2 = pd.DataFrame(result, columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                df = pd.concat([df, df2])

        df.set_index('Item ID', inplace=True, drop=True)
        print(f"\n\n\n\nList ID = {currentList.listid}\nList name = {currentList.listname} \n{df}")
        
        # ---- EditListMenu Fxn ---- 
        edited = False
        while edited == False:
            print("\n\n\n----- Edit list ------\n\n1 --- Remove item from list\n2 --- Change list name\n3 --- Delete list\n4 --- Back to main menu\n")
            editListMenu = input("Please type in a number from the menu: ")
            if editListMenu == "1":
                removeListItem(cursor, database, currentList)
            elif editListMenu == "2":
                updateListName(cursor, database, currentList)
            elif editListMenu == "3":
                edited = deleteList(cursor, database, currentList)
            elif editListMenu == "4":
                edited = True
            else:
                print("\n\nERROR: Please select a number from the menu")

def removeListItem(cursor, database, List):
    """ Recursive function to remove as many items from user's list as requested by user """

    dropItem = input("Select the item id for the item you would like to remove: ")
    print(List.items)
    List.items = List.items.strip(f'{dropItem},')
    print(List.items)
    query = f"UPDATE lists SET listOfItemIDs = '{List.items}' WHERE listid = '{List.listid}'"
    cursor.execute(query)
    database.commit()

    removeAnotherItem = input("Would you like to remove another item? [y/n]: ")
    if (removeAnotherItem == "y") or (removeAnotherItem == "Y"):
        removeListItem(cursor, database, List, UserAccount)
    else:
        pass

def updateListName(cursor, database, List):
    """ Updates the listname variable locally and in the database """

    print(f"Current list name = {List.listname}\n")
    newListName = input("Please enter the new list name: ")
    List.listname = newListName
    query = f"UPDATE lists SET listname = '{List.listname}' WHERE listid = '{List.listid}'"
    cursor.execute(query)
    database.commit()
    print(f"\n\nList name successfully changed to {List.listname}\n")

def deleteList(cursor, database, List):
    """ Removes list instance locally and in database """

    selected = False
    while selected == False:
        deleteList = input(f"Are you sure you want to delete {List.listname}? [y/n]: ")
        if (deleteList == "y") or (deleteList == "Y"):
            query = f"DELETE FROM lists WHERE listid = {List.listid}"
            cursor.execute(query)
            database.commit()
            selected = True
            return True
        elif (deleteList == "n") or (deleteList == "N"):
            selected = True
            return False
        else:
            print("\nERROR: incorrect selection. Type y or n to confirm or deny removal\n")


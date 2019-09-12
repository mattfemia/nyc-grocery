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
    """ Creates new list locally and in rdb. User can add item directly or by searching inventory
    of a specific vendor """
    
    listname = input("Please enter a name for the list: ")
    userList = {}
    dbList = []
    total = 0.00

    try:
        query = ("INSERT INTO lists (userid, listname, totalCost) " "VALUES (%s, %s, %s)")
        values = (UserAccount.userid, listname, total)
        cursor.execute(query, values)
    except mysql.connector.Error as err:
        print("\nList unsuccessfully created")
        returnSQLError(err)
    else:
        database.commit()
        UserAccount.listCount += 1
        query = "UPDATE accounts SET listcount = (%s) WHERE userid = %s"
        cursor.execute(query, (UserAccount.listCount, UserAccount.userid))
        database.commit()
    
    query = "SELECT listid FROM lists WHERE listname = %s;"
    cursor.execute(query, (listname,))
    result = cursor.fetchall()
    unpack = result[0]
    listid = unpack[0]
    print(f"LIST ID = {listid}")
    print(listid)
    
    
    lookupMethod = createListMenu()
    
    optionSelect = False
    while optionSelect is False:
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
            while userSelection is False:
                optionSelect = itemLookup(cursor, Item)
                if optionSelect is True:
                    userList[f"{Item.itemname}"] = f"{Item.price} / {Item.unit}"
                    print(f"\n{Item.itemname} successfully added to {listname}!")
                    print(f"\n\nUser list = \n{userList}\n\n")
                    dbList.append(Item.itemid)
                    
                    query = "INSERT INTO listDetails (listid, itemid, quantity, pricePerUnit) VALUES (%s, %s, 1, %s)"
                    cursor.execute(query, (listid, Item.itemid, Item.price))
                    database.commit()
                                        
                    userSelection = addAnotherItem()
                    optionSelect = userSelection
                    print("\n\n")
                else:
                    userSelection = addAnotherItem()
                    optionSelect = userSelection

        else:
            print("\n\nERROR: Invalid option selected. Please type 1 or 2 and then hit enter.")
            lookupMethod = createListMenu()

def viewLists(cursor, database, UserAccount):
    """ Queries all itemids in each user's list and stitches together itemid, itemname, storename, category, 
    price, unit into a formatted structure """

    currentItem = Item()
    currentList = GroceryList()
    
    query = "SELECT userid, listid, listname FROM lists WHERE userid = %s"
    cursor.execute(query, (UserAccount.userid,))
    result = cursor.fetchall()
    print(result)


    #TODO: This is only accounting for a user having one list -- make it so the user selects which list to edit
    #TODO: Restructure database to have an ORDERS table --> then reference that table through orderid belonging to userid 'x'
    
    for entry in result:
        currentList.listid = entry[1]
        currentList.listname = entry[2]

        df = pd.DataFrame(columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
        
        listContainer = []
    
        #TODO: Select only unique listid
        query = "SELECT itemid FROM listdetails INNER JOIN lists ON listdetails.listid = lists.listid WHERE lists.listid = %s"
        cursor.execute(query, (currentList.listid,))
        listItems = cursor.fetchall()
        for item in listItems:
            print("item = " + item)
            unpack = item[0]
            listContainer.append(unpack)
            print(listContainer)

        currentList.items = listContainer
        
        for item in currentList.items:
            if (item != ",") and (item != " "):
                
                currentItem.itemid = item
                query = "SELECT itemid, itemname, storename, category, price, unit FROM items INNER JOIN stores ON items.storeid = stores.storeid WHERE itemid = %s"
                cursor.execute(query, (currentItem.itemid,))
                result = cursor.fetchall()
                df2 = pd.DataFrame(result, columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                df = pd.concat([df, df2])

        df.set_index('Item ID', inplace=True, drop=True)

        
        print(f"\n\nList ID = {currentList.listid}\nList name = {currentList.listname} \n{df}")

    # -------- editList function ----------

    edit = input("\n\nWould you like to edit your lists? [y/n]: ")
    if (edit == "y") or (edit == "Y"):

        # TODO: Disable user from accessing lists outside of their own (currently can type any list id and retrieve it)
        validList = False
        while validList is False:
            listSelect = input("Please enter the List ID shown above the list you would like to edit: ")
            if int(listSelect) in UserAccount.lists:
                currentList = GroceryList()
                listContainer = []
                query = "SELECT itemid FROM listdetails INNER JOIN lists ON listdetails.listid = lists.listid WHERE userid = %s"
                cursor.execute(query, (UserAccount.userid,))
                listItems = cursor.fetchall()
                for item in listItems:
                    unpack = item[0]
                    listContainer.append(unpack)

                currentList.items = listContainer

                query = "SELECT userid, listid, listname FROM lists WHERE listid = %s"
                cursor.execute(query, (listSelect,))
                result = cursor.fetchall()

                for entry in result:
                    currentList.listid = entry[1]
                    currentList.listname = entry[2]

                df = pd.DataFrame(columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                for item in currentList.items:
                        
                    currentItem.itemid = item
                    query = "SELECT itemid, itemname, storename, category, price, unit FROM items INNER JOIN stores ON items.storeid = stores.storeid WHERE itemid = %s"
                    cursor.execute(query, (currentItem.itemid,))
                    result = cursor.fetchall()
                    df2 = pd.DataFrame(result, columns=['Item ID', 'Item', 'Store Name', 'Category', 'Price', 'Unit'])
                    df = pd.concat([df, df2])

                df.set_index('Item ID', inplace=True, drop=True)
                print(f"\n\n\n\nList ID = {currentList.listid}\nList name = {currentList.listname} \n{df}")

                editLists(cursor, database, currentList)
                
                validList = True
            else:
                retry = input("You do not have a list ID matching your input. Retry? [y/n]")
            
                if (retry == "y") or (retry == "Y"):
                    validList = False
                else:
                    validList = True

def editLists(cursor, database, List):
    """ Collection of functions organized statically in menu: removeListItem(), 
    updateListName(), editListMenu() """ 
    
    edited = False
    while edited == False:
        print("\n\n\n----- Edit list ------\n\n1 --- Remove item from list\n2 --- Change list name\n3 --- Delete list\n4 --- Back to main menu\n")
        editListMenu = input("Please type in a number from the menu: ")
        if editListMenu == "1":
            removeListItem(cursor, database, List)
        elif editListMenu == "2":
            updateListName(cursor, database, List)
        elif editListMenu == "3":
            edited = deleteList(cursor, database, List)
        elif editListMenu == "4":
            edited = True
        else:
            print("\n\nERROR: Please select a number from the menu")

def removeListItem(cursor, database, List):
    """ Recursive function to remove as many items from user's list as requested by user """

    if List.items:
        dropItem = input("Select the item id for the item you would like to remove: ")
        print(List.items)
        List.items = List.items.strip(f'{dropItem},')
        print(List.items)
        query = "UPDATE lists SET listOfItemIDs = %s WHERE listid = %s"
        cursor.execute(query, (List.items, List.listid))
        database.commit()

        removeAnotherItem = input("Would you like to remove another item? [y/n]: ")
        if (removeAnotherItem == "y") or (removeAnotherItem == "Y"):
            removeListItem(cursor, database, List)
        else:
            pass
    else:
        print("\n\nNo items in list yet!")

def updateListName(cursor, database, List):
    """ Updates the listname variable locally and in the database """

    print(f"Current list name = {List.listname}\n")
    newListName = input("Please enter the new list name: ")
    List.listname = newListName
    query = "UPDATE lists SET listname = %s WHERE listid = %s"
    cursor.execute(query, (List.listname, List.listid))
    database.commit()
    print(f"\n\nList name successfully changed to {List.listname}\n")

def deleteList(cursor, database, List):
    """ Removes list instance locally and in database """

    selected = False
    while selected is False:
        deleteList = input(f"Are you sure you want to delete {List.listname}? [y/n]: ")
        if (deleteList == "y") or (deleteList == "Y"):
            query = "DELETE FROM lists WHERE listid = %s"
            cursor.execute(query, (List.listid,))
            database.commit()
            selected = True
            return True
        elif (deleteList == "n") or (deleteList == "N"):
            selected = True
            return False
        else:
            print("\nERROR: incorrect selection. Type y or n to confirm or deny removal\n")

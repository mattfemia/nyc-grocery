from grocery import *
# TODO: Remove/change hours columns from STORES table
# TODO: Add address column to STORES table
# TODO: Create a list class
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

def mainMenu(username):
    """ Prints the main menu options to the terminal """
    print("\n\n\n\n\n~~ Welcome " + username + "! ~~ \n\nWhat would you like to do?")
    print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n")

    navigate = input("Please enter a number in the menu: ")

    while (navigate != "1") & (navigate != "2") & (navigate != "3") & (navigate != "4") & (navigate != "5"):
        print("\n\nERROR: Please select one of the current menu options \n")
        print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n")

        navigate = input("Please enter a number in the menu: ")

    print("\n\n")

    return navigate

def createlist(cursor, database, UserAccount, Store, Item):
    """ Creates new list locally and in rdb """
    
    listname = input("Please enter a name for the list: ")
    userList = {}
    lookupMethod = input("\n1 --- Select store location\n\n2 --- Lookup item\n")
    
    optionSelect = False
    while optionSelect == False:
        if lookupMethod == "1":

            #TODO: GIVE OPTION TO SELECT STORE BY NEIGHBORHOOD, LIST ALL STORES, ETC (query location table instead)

            try:
                storeName = input("Enter the name of the store: ")
                storeName += "%"
                query = f"SELECT storeid, storename, address FROM stores WHERE storename LIKE '{storeName}' ORDER BY storename ASC"
                cursor.execute(query)

                # Give option to select inventory
                # --- 
            except IndexError:
                print("ERROR: Store not found")
                lookupMethod = input("\n1 --- Select store location\n\n2 --- Lookup item\n")
            else:
                optionSelect = True
                storeResults = cursor.fetchall()
                unpack = storeResults[0]
                (storeid, storename, address) = unpack

                # Testing for perfect user entry:
                Store.storeid = storeid
                Store.storename = storename
                Store.address = address

                #TODO: List all stores matching wildcard and display
                # --- 

                userSelection = False
                while userSelection == False:
                    print("Options: \n")
                    storeSelect = input(f'{Store.storeid} ---' + " " + Store.storename + " @ " + Store.address + "\nSelect a store number: ")
                    
                    if storeSelect == "1": # Dummy statement --------------------------------
                        print("Success")
                        userSelection = True
                    else:
                        print("\nERROR: Invalid selection")

                    print("\n\n")

        elif lookupMethod == "2":
            try:
                itemName = input("Enter the name of the item: ")
                itemName += "%"

                # JOIN query
                # --- 

                query = f"SELECT itemid, itemname, price, unit, productSize, storeid FROM items WHERE itemname LIKE '{itemName}' ORDER BY itemname ASC"
                cursor.execute(query)
            except:
                print("ERROR: Item not found")
                lookupMethod = input("\n1 --- Select store location\n\n2 --- Lookup item\n")
            else:
                # TODO: Return all objects not just one
                # Enumerate query results?

                optionSelect = True
                itemResults = cursor.fetchall()
                unpack = itemResults[0]
                (itemid, itemname, price, unit, productSize, storeid) = unpack

                # TODO: User selects which item
                # --- 

                Item.itemid = itemid
                Item.itemname = itemname
                Item.price = price
                Item.unit = unit
                Item.productSize = productSize
                Item.storeid = storeid

                userSelection = False
                while userSelection == False:
                    print("\n\nOptions: \n")
                    itemSelection = input(f'\n{Item.itemid} ---' + " " + Item.itemname + " @ " + str(Item.price) + " per " + Item.unit + "\nSelect an item to add to your list: ")
                    
                    if itemSelection == "1": # Dummy statement --------------------------------
                        userList[f"{Item.itemname}"] = f"{Item.price} / {Item.unit}"
                        print(f"\n{Item.itemname} successfully added to {listname}!")
                        print(f"\n\nUser list = \n{userList}\n\n")
                        userSelection = True
                    else:
                        print("\nERROR: Invalid selection")

                    print("\n\n")

        else:
            print("ERROR: Invalid option selected. Please type 1 or 2 and then hit enter.")
            lookupMethod = input("\n1 --- Select store location\n\n2 --- Lookup item\n")
            
    #TODO: Create lookup item function and embed inside of this function

    """ 
        - Select store
            - Query locations, then lookup
        - Lookup item


    - Prompt:
        - Next item
            - Repeat lookup item options
        - End list
            - Push sql commit query to user list
    """
    
    # cursor.execute(f"INSERT INTO lists (userid, listname) VALUES {UserAccount.userid, listname}")
    # database.commit()
    # UserAccount.listcount += 1
    # cursor.execut(f"INSERT INTO accounts (listcount) VALUES ({UserAccount.listcount})")
    # database.commit()
        

def priceLookup(item, database):
    """ If grocery item is in the 'database', print the price of the item """
    try:
        print("Price of " + f'{item}' + " = " + "$" + f'{database[item]}')
    except:
        print("Item is not currently in our database \nPlease try a different item")

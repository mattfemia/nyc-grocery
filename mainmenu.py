from grocery import *
# TODO: Remove/change hours columns from STORES table
# TODO: Add address column to STORES table


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

def createlist(cursor, database, UserAccount):
    """ Creates new list locally and in rdb """
    
    listname = input("Please enter a name for the list: ")
    userList = {}
    lookupMethod = input("\n1.) Select store location\n\n 2.) Lookup item\n")
    
    optionSelect = False
    while optionSelect == False:
        if lookupMethod == 1:
            storeName = input("Enter the name of the store: ")
            query = "SELECT"
            # Query storeName and return all results of that store
            # Select exact store
            # Give option to select inventory
        elif lookupMethod == 2:
            itemName = input("Enter the name of the item: ")
            # Query the itemName in items DB
            # Return all items containing that name with wildcard query
            # order by price ascending
            # Prompt user to select the exact item
            # Append userList with itemid
        else:
            print("ERROR: Store not found")
            lookupMethod = input("\n1.) Select store location\n\n 2.) Lookup item\n")

    #TODO: Create lookup item function and embed inside of this function

    """ 
    - Store listname
    - Create a dict object
    - Give options:
        - Select store
            - Query locations, then lookup
        - Lookup item
    - Query for item id
    - Append list object with item id
    - Print out current list of items
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

from grocery import *

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

def priceLookup(item, database):
    """ If grocery item is in the 'database', print the price of the item """
    try:
        print("Price of " + f'{item}' + " = " + "$" + f'{database[item]}')
    except:
        print("Item is not currently in our database \nPlease try a different item")

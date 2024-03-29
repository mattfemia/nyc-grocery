def startMenu():
    """Prompts the main menu options to load"""

    print("\nWelcome to NYC Groceries! \n")
    print("\n1 --- Sign-in ---\n\nOR\n\n2 --- Sign-up ---\n\n")

    startmenu = input("Please type in a number from the menu:")
    print("\n\n")

    while (startmenu != "1") & (startmenu != "2"):
        print("\n\nERROR: Please select one of the current menu options \n")
        startMenu()

    return startmenu

def mainMenu(username):
    """ Prints the main menu options to the terminal """
    
    print("\n\n\n\n~~ Welcome " + username + "! ~~ \n\nWhat would you like to do?")
    print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n6 --- Logout\n7 --- Quit\n")

    navigate = input("Please enter a number in the menu: ")

    while (navigate != "1") & (navigate != "2") & (navigate != "3") & (navigate != "4") & (navigate != "5") & (navigate != "6") & (navigate != "7"):
        print("\n\nERROR: Please select one of the current menu options \n")
        print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n6 --- Logout\n7 --- Quit\n")

        navigate = input("Please enter a number in the menu: ")

    print("\n\n")

    return navigate

def createListMenu():
    """ Simple menu displayed when selecting "Create a new list" """

    lookupMethod = input("\n1 --- Select store location\n\n2 --- Lookup item\nChoose your lookup method: ")
    return lookupMethod

def accountMenu():
    """ Displays options for account management """

    print("\n\n# --- User account settings --- #\n\n1 --- Change username\n2 --- Reset password\n3 --- Update email address\n4 --- Update name\n5 --- Delete Account\n6 --- Back to main menu")
    option = input("Please select an option: ")

    return option
    
#TODO: Setup all database tables
#TODO: Mainmenu functionality
#TODO: Figure out how to split into multiple files

#!!!!! SET ENVIRONMENT VARIABLE DATABASE_PW OR PROG WILL NOT RUN !!!!!

import mysql.connector
import os

def connectdb():
    password = os.getenv("DATABASE_PW")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=password,
        auth_plugin='mysql_native_password',
        database="Grocery"
    )

    db = mydb.cursor()

    return db

def loadStartMenu():
    """Prompts the main menu options to load"""

    print("\nWelcome to East Village groceries! \n")
    print("\n1 --- Sign-in ---\n\nOR\n\n2 --- Sign-up ---\n\n")

    startmenu = input("Please type in a number from the menu:")
    print("\n\n")

    while (startmenu != "1") & (startmenu != "2"):
        print("\n\nERROR: Please select one of the current menu options \n")
        print("\n1 --- Sign-in ---\n\nOR\n\n2 --- Sign-up ---\n\n")

        startmenu = input("Please type in a number from the menu: ")

    return startmenu

def signup():
    """ Setup user account with username, password, email"""
    username = input("Please enter a username: ")
    # if username in database already --> throw error, re-prompt
    # else store in database
    password = input("Please enter a password: ")
    # if password doesn't meet requirements --> throw error, re-prompt
    # else store in database
    email = input("Please enter your email address: ")
    # if email is invalid (formatting) --> throw error, re-prompt
    # else store in database

    print("\n\n" + username + "'s account successfully created!")

    return username

def signin():
    username = input("Username: ")
    # if username not in database, throw error message --> retry? or signup?
    # else password
    password = input("Password: ")
    # if password doesn't match users, throw error message --> retry or ..........?
    print("\n\n")

    return username

def mainMenu(username):
    """ Prints the main menu options to the terminal """
    print("\n~~ Welcome " + username + "! ~~ \n\nWhat would you like to do?")
    print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n")

    navigate = input("Please enter a number in the menu: ")

    while (navigate != "1") & (navigate != "2") & (navigate != "3") & (navigate != "4") & (navigate != "5"):
        print("\n\nERROR: Please select one of the current menu options \n")
        print("1 --- Edit/view my grocery lists\n2 --- Create a new list\n3 --- Lookup item\n4 --- Show all available items\n5 --- Account settings\n")

        navigate = input("Please enter a number in the menu: ")

    print("\n\n")

    return navigate

def priceLookup(item):
    """ If grocery item is in the 'database', print the price of the item """
    try:
        print("Price of " + f'{item}' + " = " + "$" + f'{unionMarket[item]}')
    except:
        print("Item is not currently in our database \nPlease try a different item")

# TODO: Update user class based on accounts table in database
class User:
    def __init__(self):
        self.user = self
        self.location = "East Village" # TODO: Update this to apply to all locations
        self.lists = []

    def setLocation(self, newLocation):
        """ Defines user's location for stores """
        if newLocation in locations:
            self.location = newLocation
            print("User location updated successfully.")
        else:
            print("Sorry, this location is not currently setup in our database. \nPlease try a different location")

    def addList(self, newList):
        """ Saves current list to user's list database """
        def saveList(shoppingList):
            if type(shoppingList) == GroceryList:
                try:
                    lists.append(newList)
                except:
                    print("Error: list could not be saved. Check to make sure it exists")
            else:
                print("Error: List could not be saved.")
    
        
class GroceryList:
    def __init__(self):
        self.user = username
        self.listName = "Grocery List"
        self.total = 0.00
        self.numOfItems = 0
        self.cart = []
        
    def addToCart(self, *listItems):
        """ Appends the main groceryList data structure """
        for item in listItems:
            if item in unionMarket: # TODO: Update this to apply to all locations
                self.cart.append(item)
                self.total += unionMarket[item]
                self.numOfItems += 1
                print(item + " = " + f'{unionMarket[item]}')
            else:
                print("Item not currently in database")
    def printTotal(self):
        """ Formats the total cost to currency """
        print("Your total = $" + f'{round(self.total, 2)}')


# ---------- PROGRAM BEGINS HERE ---------- #

db = connectdb()

navigate = loadStartMenu()

if navigate == "1":
    username = signin()
elif navigate == "2":
    username = signup()

navigate = mainMenu(username)

if navigate == "1":
    print("Edit/view my grocery lists")
elif navigate == "2":
    print("Create a new list")
elif navigate == "3":
    print("Lookup item")
elif navigate == "4":
    print("Create a new list")
elif navigate == "5":
    print("Show all available")




# ----TESTING----

locations = ["East Village"] # placeholder for testing

unionMarket = {"Milk": 4.99, "Eggs": 3.79, "Bananas": 2.16} # placeholder for testing



myList = GroceryList()
myList.addToCart("Milk", "Eggs")
print(myList.cart)
myList.printTotal()
print(myList.numOfItems)
priceLookup("Milk")
# user1 = User()
# user1.setLocation("East Village")

# print(user1.user)
#TODO: Setup user database
#TODO: Setup grocery store database
#TODO: Setup user login under user class

#!!!!! SET ENVIRONMENT VARIABLE DATABASE_PW OR PROG WILL NOT RUN !!!!!

import mysql.connector
import os

# Setup database connection
password = os.getenv("DATABASE_PW")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=password,
    auth_plugin='mysql_native_password',
    database="Grocery"
)

# Database instance
db = mydb.cursor()



def makeAccount():
    """ Setup username and NYC location """
    currentUser = 'Fred'
    return currentUser

def priceLookup(item):
    """ If grocery item is in the 'database', print the price of the item """
    try:
        print("Price of " + f'{item}' + " = " + "$" + f'{unionMarket[item]}')
    except:
        print("Item is not currently in our database \nPlease try a different item")


        
class User:
    def __init__(self):
        self.user = self
        self.location = "East Village"
        self.lists = []
    def setLocation(self, newLocation):
        if newLocation in locations:
            self.location = newLocation
            print("User location updated successfully.")
        else:
            print("Sorry, this location is not currently setup in our database. \nPlease try a different location")
    def addList(self, newList):
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
            if item in unionMarket:
                self.cart.append(item)
                self.total += unionMarket[item]
                self.numOfItems += 1
                print(item + " = " + f'{unionMarket[item]}')
            else:
                print("Item not currently in database")
    def printTotal(self):
        """ Formats the total cost to currency """
        print("Your total = $" + f'{round(self.total, 2)}')
         

locations = ["East Village"]
username = makeAccount()

unionMarket = {"Milk": 4.99, "Eggs": 3.79, "Bananas": 2.16}



# ----TESTING----
# Sanity check

# myList = groceryList()
# myList.addToCart("Milk", "Eggs")
# print(myList.cart)
# myList.printTotal()
# print(myList.numOfItems)
priceLookup("Milk")
user1 = User()
user1.setLocation("East Village")

print(user1.user)




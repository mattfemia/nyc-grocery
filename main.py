
import mysql.connector
import os
from grocery import *

# ---------- PROGRAM BEGINS HERE ---------- #

password = os.getenv("DATABASE_PW")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=password,
    auth_plugin='mysql_native_password',
    database="Grocery"
)

db = mydb.cursor()

# ---------- Start menu ------------ #
navigate = loadStartMenu()

currentUser = UserAccount()

if navigate == "1":
    currentUser.username = signin()
elif navigate == "2":
    newUserName = input("Please enter a username: ")
    currentUser.checkUsername(newUserName, db)

currentUser.username = newUserName
currentUser.updateUsername(currentUser.username, db, mydb)


# ---------- Main Menu ---------- #
navigate = mainMenu(newUserName)

if navigate == "1":
    print("Edit/view my grocery lists\n")
elif navigate == "2":
    print("Create a new list\n")
elif navigate == "3":
    print("Lookup item\n")
elif navigate == "4":
    print("Create a new list\n")
elif navigate == "5":
    print("Show all available\n")




# ----TESTING----

locations = ["East Village"] # placeholder for testing

database = {"Milk": 4.99, "Eggs": 3.79, "Bananas": 2.16} # placeholder for testing



myList = GroceryList()
myList.user = currentUser.username
myList.addToCart(database, "Milk", "Eggs")

print("My cart = ", end='')
for item in myList.cart:
    print(item + " ", end='')
print("\n")
myList.printTotal()
print(myList.numOfItems)
priceLookup("Milk", database)
# user1 = User()
# user1.setLocation("East Village", locations)

# print(user1.user)
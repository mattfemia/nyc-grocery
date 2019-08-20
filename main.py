
import mysql.connector
import os
from grocery import *

# ---------- PROGRAM BEGINS HERE ---------- #

db = connectdb()

navigate = loadStartMenu()

if navigate == "1":
    username = signin()
elif navigate == "2":
    username = signup()

navigate = mainMenu(username)

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
myList.user = username
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
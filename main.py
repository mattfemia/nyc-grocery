
import mysql.connector
import os
from account import *
from mainmenu import *
from menu import *
from validate_email import validate_email
from disposable_email_domains import blocklist

# ---------- PROGRAM BEGINS HERE ---------- #

password = os.getenv("DATABASE_PW")
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=password,
    auth_plugin='mysql_native_password',
    database="Grocery"
)

cursor = database.cursor()

# ---------- Start menu ------------ #
navigate = startMenu()

currentUser = UserAccount()

# signin or signup
if navigate == "1":
    signin(cursor, currentUser)
elif navigate == "2":
    newUserName = input("Please enter a username: ") 
    currentUser.createAccount(newUserName, cursor, database, currentUser)

print(currentUser.userid)

# ---------- Main Menu ---------- #
navigate = mainMenu(currentUser.username)
currentStore = Store()
currentItem = Item()

if navigate == "1":
    print("Edit/view my grocery lists\n")
elif navigate == "2":
    createlist(cursor, database, currentUser, currentStore, currentItem)
elif navigate == "3":
    priceLookup(cursor)
elif navigate == "4":
    showAllItems(cursor, currentItem)
elif navigate == "5":
    print("Account settings\n")
elif navigate == "6":
    print("Sign-out")
elif navigate == "7":
    print("Quit")

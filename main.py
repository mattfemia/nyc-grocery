
import mysql.connector
import os
from validate_email import validate_email
from disposable_email_domains import blocklist

# Local file dependencies
from accounts import *
from items import *
from menus import *
from lists import *

# ------------ PROGRAM BEGINS HERE ------------ #

password = os.getenv("DATABASE_PW")
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=password,
    auth_plugin='mysql_native_password',
    database="grocery_test"
)

cursor = database.cursor()

# ------------ Start menu ------------ #

entry = False
while entry == False:
    navigate = startMenu()
    currentUser = UserAccount()
    if navigate == "1":
       entry = signin(cursor, currentUser)
    elif navigate == "2":
        newUserName = input("Please enter a username: ") 
        entry = currentUser.createAccount(newUserName, cursor, database, currentUser)

# ------------ Main Menu ------------ #
exitProgram = False
while exitProgram == False:
    navigate = mainMenu(currentUser.username)
    currentStore = Store()
    currentItem = Item()

    if navigate == "1":
        viewLists(cursor, database, currentUser)
    elif navigate == "2":
        createlist(cursor, database, currentUser, currentStore, currentItem)
    elif navigate == "3":
        priceLookup(cursor)
    elif navigate == "4":
        showAllItems(cursor, currentItem)
    elif navigate == "5":
        accountSettings(cursor, database, currentUser)
    elif navigate == "6":
        navigate = startMenu()
    elif navigate == "7":
        print("Exiting program ...\n\n\n\n")
        exitProgram = True

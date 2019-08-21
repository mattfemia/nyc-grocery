#TODO: Mainmenu functionality
#TODO: Figure out how to split into multiple files

#!!!!! SET ENVIRONMENT VARIABLE DATABASE_PW OR PROG WILL NOT RUN !!!!!

import mysql.connector
import os
from validate_email import validate_email
from disposable_email_domains import blocklist
from datetime import datetime

# Temporarily placing inside main.py to avoid -- ReferenceError: weakly-referenced object no longer exists
# def connectdb():
#     password = os.getenv("DATABASE_PW")
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd=password,
#         auth_plugin='mysql_native_password',
#         database="Grocery"
#     )

#     db = mydb.cursor()

#     return db

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

def signup(cursor):
    """ Setup user account with username, password, email"""
    username = input("Please enter a username: ")
    cursor.execute("SELECT username FROM accounts WHERE username = username")
    result = cursor.fetchall()
    if result:
        print("Name is in database!")
    else:
        print("Name is not in database")

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

class UserAccount:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.phone = ""
        self.listCount = 0
        self.registrationDate = ""
        self.userid = 0

    def checkUsername(self, username, cursor, UserAccount):
        """ Send query to database to check if username already exists. If query returns no value
        username is saved to current user's account """
        
        cursor.execute(f"SELECT username FROM accounts WHERE username = '{username}' ")
        result = cursor.fetchall()
        while len(result) != 0:
            print("\n\n\n\n\nSorry that username is currently unavailable\n")
            username = input("Please select another username: ")
            cursor.execute(f"SELECT username FROM accounts WHERE username = '{username}' ")
            result = cursor.fetchall()
        UserAccount.username = username

    def createPassword(self, UserAccount):
        """ Validates that password and retyped passwords match. After validation, user's
        password field is updated to the chosen password """

        while UserAccount.password == "":
            password = input("\nCreate a password: ")
            retype = input("Retype password to confirm: ")
            match = (password == retype)
            print(match)
            if password == retype:
                UserAccount.password = password
            else:
                print("\nERROR: Passwords do not match\n")

    def assignEmail(self, UserAccount):
        """ Requests user to type email address. Basic validation is done on the format.
        Then updates the email field for the user's account """

        while UserAccount.email == "":
            email = input("Please enter your email address: ")
            validate = validate_email('example@example.com')
            if validate == True:
                # validEmail = False
                # while validEmail == False:
                #     if email.split('@')[1] in blocklist:
                #         message = "Please enter your permanent email address."
                #         print(message)
                #     else:
                #         validEmail == True
                UserAccount.email = email
            else:
                print("\nERROR: Invalid email. Please select your current email address")

    def userDetails(self, UserAccount):
        """ Requests first and last name, plus phone number for user. User is given option to
         update these fields or not because they are not required in the database query """

        editDetails = input("\n\nWould you like to edit your account details [y/n]: ")
        print(editDetails)
        if (editDetails == "y" or "Y" or "yes" or "Yes"):    
            firstName = input("First name: ")
            UserAccount.firstname = firstName
            lastName = input("Last name: ")
            UserAccount.lastname = lastName
            phoneNumber = input("Phone number: ")
            UserAccount.phone = phoneNumber
        UserAccount.registrationDate = datetime.today().strftime('%Y-%m-%d')

    def createAccount(self, username, cursor, database, UserAccount):
        """ Combines all the functions that request the info required to create a user's 
        account locally and in database. Fields: username, password, email, first name, 
        last name, and phone number """

        UserAccount.checkUsername(username, cursor, UserAccount)
        UserAccount.createPassword(UserAccount)
        UserAccount.assignEmail(UserAccount)
        UserAccount.userDetails(UserAccount)
        print(UserAccount.registrationDate)

        sqlcommand = f"INSERT INTO accounts (username, firstname, lastname, email, password, \
            phone, listcount, registrationdate) VALUES \
                {UserAccount.username, UserAccount.firstname, UserAccount.lastname, UserAccount.email, UserAccount.password, int(UserAccount.phone), UserAccount.listCount, str(UserAccount.registrationDate)}"
        cursor.execute(sqlcommand)
        database.commit()

        cursor.execute(f"SELECT userid FROM accounts WHERE username = '{UserAccount.username}'")
        accountID = cursor.fetchall()
        UserAccount.userid = accountID

    def updateUsername(self, username, cursor, database):
        """ Enters username value into the database """
        cursor.execute(f"INSERT INTO accounts (username) VALUES ('{username}')")
        database.commit()
        # insertUsername = "INSERT INTO accounts (username) VALUES (%s)"
        # username = username


class User:
    def __init__(self):
        self.user = self
        self.location = "East Village" # TODO: Update this to apply to all locations
        self.lists = []

    def setLocation(self, newLocation, locations):
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
        self.user = ""
        self.listName = "Grocery List"
        self.total = 0.00
        self.numOfItems = 0
        self.cart = []
        
    def addToCart(self, database, *listItems):
        """ Appends the main groceryList data structure """
        for item in listItems:
            if item in database:
                self.cart.append(item)
                self.total += database[item]
                self.numOfItems += 1
                print(item + " = " + f'{database[item]}')
            else:
                print("Item not currently in database")
    def printTotal(self):
        """ Formats the total cost to currency """
        print("Your total = $" + f'{round(self.total, 2)}')
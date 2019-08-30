#!!!!! SET ENVIRONMENT VARIABLE DATABASE_PW OR PROG WILL NOT RUN !!!!!

import mysql.connector
import os
from validate_email import validate_email
from disposable_email_domains import blocklist
from datetime import datetime

from menus import *
from items import *

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
            print("\n\n\n\n\nSorry that username is taken\n")
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
        if (editDetails == "y") or (editDetails == "Y") or (editDetails == "yes") or (editDetails == "Yes"):    
            firstName = input("First name: ")
            UserAccount.firstname = firstName
            lastName = input("Last name: ")
            UserAccount.lastname = lastName
            
            phone = False
            while phone == False:
                phoneNumber = input("Phone number: ")
                try:
                    float(phoneNumber)
                except ValueError:
                    print("Invalid phone number. Exclude dashes i.e) 3151230987")
                else:
                    UserAccount.phone = phoneNumber
                    phone = True
        else:
            UserAccount.phone = 0
        currentDate = datetime.today().strftime('%Y-%m-%d')
        UserAccount.registrationDate = currentDate

    def createAccount(self, username, cursor, database, UserAccount):
        """ Combines all the functions that request the info required to create a user's 
        account locally and in database. Fields: username, password, email, first name, 
        last name, and phone number """

        UserAccount.checkUsername(username, cursor, UserAccount)
        UserAccount.createPassword(UserAccount)
        UserAccount.assignEmail(UserAccount)
        UserAccount.userDetails(UserAccount)

        try:
            query = f"INSERT INTO accounts (username, firstname, lastname, email, password, \
            phone, listcount, registrationdate) VALUES \
                {UserAccount.username, UserAccount.firstname, UserAccount.lastname, UserAccount.email, UserAccount.password, int(UserAccount.phone), UserAccount.listCount, str(UserAccount.registrationDate)}"
            cursor.execute(query)
        except:
            print("ERROR: Please try again later")
            return False
        else:
            database.commit()
            cursor.execute(f"SELECT userid FROM accounts WHERE username = '{UserAccount.username}'")
            accountID = cursor.fetchall()
            UserAccount.userid = accountID
            return True

    def updateUsername(self, username, cursor, database):
        """ Enters username value into the database """
        cursor.execute(f"INSERT INTO accounts (username) VALUES ('{username}')")
        database.commit()
        # insertUsername = "INSERT INTO accounts (username) VALUES (%s)"
        # username = username


def signin(cursor, UserAccount):
    """ Queries database against the credentials provided and either validates or
    denies user access to login. Upon login, UserAccount object is created and
    populated with all corresponding User variables """

    accountValid = False
    while accountValid == False:
        try:
            username = input("Username: ")
            password = input("Password: ")
            print(username)
            username = f"{username}"
            print(username)
            cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
        except mysql.connector.errors.ProgrammingError:
            print("ERROR: Account information is not valid")
            accountValid = False
            return accountValid
        else:
            result = cursor.fetchall() 
            if result:
                unpack = result[0] 
                (userid, user, first, last, email, pw, phone, listcount, regdate) = unpack
                UserAccount.userid = userid
                UserAccount.username = user
                UserAccount.firstname = first
                UserAccount.lastname = last
                UserAccount.email = email
                if pw != password:
                    print("\n\n----- ERROR: Information is not valid. Please retry or signup for an account -----")
                    accountValid = False
                    return accountValid
                else:
                    UserAccount.password = pw
                    UserAccount.phone = phone
                    UserAccount.listCount = listcount
                    UserAccount.registrationDate = regdate
                    print("Success!")
                    accountValid = True
                    return accountValid
            else:
                print("\n\n----- ERROR: Account information is not valid. Please retry or signup for an account -----\n")
                accountValid = False
                return accountValid
            print("\n\n")

def accountSettings(cursor, database, UserAccount):
    """ Menuing function that lists a collection of UserAccount CRUD functions 
    -- aside from creating an account """
    
    menuSelect = False
    while menuSelect == False:
        option = accountMenu()    
        
        if option == "1":
            updateUsername(cursor, database, UserAccount)
        elif option == "2":
            resetPassword(cursor, database, UserAccount)
        elif option == "3":
            updateEmail(cursor, database, UserAccount)
        elif option == "4":
            updateName(cursor, database, UserAccount)
        elif option == "5":
            deleteAccount(cursor, database, UserAccount)
        elif option == "6":
            menuSelect = True
        else:
            print("\nERROR: Please enter one of the numbers from the menu\n\n")

def updateUsername(cursor, database, UserAccount):
    """ Updates username locally and in database """

    newUserName = input("\nPlease enter new username: ")
    retype = input("\nPlease retype new username: ")
    confirm = False
    while confirm == False:
        if newUserName == retype:
            try:
                UserAccount.username = newUserName
                query = f"UPDATE accounts SET username = '{UserAccount.username}' WHERE userid = '{UserAccount.userid}'"
                cursor.execute(query)
            except:
                print("ERROR: Username could not be updated please try again later")
            else:
                database.commit()
                print(f"\n\nUsername successfully updated to: {UserAccount.username}\n")
                confirm = True
        else:
            print("ERROR: Usernames do not match. Please try again")

def resetPassword(cursor, database, UserAccount):
    """ Prompts user to verify current password and then select a new password. Result is
    updated locally and in database """

    oldPassword = input("\nPlease enter old password: ")
    if oldPassword == UserAccount.password:
        matchingPasswords = False
        while matchingPasswords == False:
            newPassword = input("\nPlease enter new password: ")
            retype = input("Please retype new password: ")
            if newPassword == retype:
                matchingPasswords = True
                UserAccount.password = newPassword
                try:
                    query = f"UPDATE accounts SET password = '{UserAccount.password}' WHERE userid = '{UserAccount.userid}'"
                    cursor.execute(query)
                except:
                    print("\nERROR: Password could not be updated. Please try again later.\n")
                else:
                    database.commit()
                    print("\n\nPassword successfully updated.")
            else:
                print("\nError passwords do not match")
                tryAgain = input("Try again? [y/n]")
                if (tryAgain == "y") or (tryAgain == "Y"):
                    matchingPasswords = False
                elif (tryAgain == "n") or (tryAgain == "N"):
                    matchingPasswords = True
                else:
                    print("\nERROR: Please enter y or n")
    else:
        print("ERROR: incorrect password submitted")   
        
def updateEmail(cursor, database, UserAccount):
    """ Allows user to update field of choice. UserAccount detail is chosen
    by the userField argument """

    newEmail = input(f"\nPlease enter the new email address: ")
    UserAccount.email = newEmail
    try:
        query = f"UPDATE accounts SET email = '{UserAccount.email}' WHERE userid = '{UserAccount.userid}'"
        cursor.execute(query)
    except:
        print(f"\nERROR: Email address could not be updated. Please try again later")
    else:
        database.commit()
        print(f"\n\nEmail address updated successfuly.")

def updateName(cursor, database, UserAccount):
    """ Updates first and last name UserAccount fields """

    first = input(f"\nFirst name: ")
    UserAccount.firstname = first

    last = input(f"Last name: ")
    UserAccount.lastname = last

    try:
        query = f"UPDATE accounts SET firstname = '{UserAccount.firstname}' WHERE userid = '{UserAccount.userid}'"
        cursor.execute(query)
    except:
        print(f"\nERROR: Name could not be updated. Please try again later")
    else:
        database.commit()

    try:
        query = f"UPDATE accounts SET lastname = '{UserAccount.lastname}' WHERE userid = '{UserAccount.userid}'"
        cursor.execute(query)
    except:
        print(f"\nERROR: Name could not be updated. Please try again later")
    else:
        database.commit()
        print(f"\n\nName updated successfuly.")

def deleteAccount(cursor, database, UserAccount):
    """ Deletes account locally and in database. Then ends the program """

    challenge = False
    while challenge == False:
        passwordChallenge = input("\nPlease enter your password: ")
        if passwordChallenge == UserAccount.password:
            confirmDelete = input("\nAre you sure you want to delete your account? [y/n]: ")
            if (confirmDelete == "y") or (confirmDelete == "Y"):
                query = f"DELETE a, l FROM accounts as a INNER JOIN lists as l on a.userid = l.userid WHERE a.userid = '{UserAccount.userid}'"
                cursor.execute(query)
                database.commit()

                UserAccount.username = ""
                UserAccount.password = ""
                UserAccount.firstname = ""
                UserAccount.lastname = ""
                UserAccount.email = ""
                UserAccount.phone = ""
                UserAccount.listCount = 0
                UserAccount.registrationDate = ""
                UserAccount.userid = 0

                print("Account successfully deleted.\n\n\nExiting program...\n\n")
                challenge = True
                exit()
            elif (confirmDelete == "n") or (confirmDelete == "N"):
                challenge = True
            else:
                print("\nERROR: Please type y or n")
        else:
            print("\nERROR: Passwords don't match")
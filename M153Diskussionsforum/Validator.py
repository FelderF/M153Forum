from sqlite3 import sqlite_version_info
from sqlQuerries import SQLQuerries
#used for different input validations
#can be called and returns true if the criteria is met, false otherwise

class Validator(object):   
    
    #tests if input is empty, returns false if it is empty, true otherwise
    def isNotEmpty(self, input):
        if input:
            return True
        else:
            return False
    
    #tests if the input string contains at least one number, is used for the password validation
    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    #test if password meets criteria, returns true if the password is valid, false otherwise and prints the correspondnig error messages
    #is used in the registration process
    def isValidPassword(self, password):  
        #min 12 characters, at least one lowercase, uppercase, number. Each test writes error and returns false if something is wrong
        #test if at leas 12 characters and maximum 99
        length = len(password)
        if (length >12 or length <100):
            validLength = True
        #test if on lowercase
        for c in password:
            if c.islower():
                hasLowercase = True
        #test if one uppercase
        for c in password:
            if c.isupper():
                hasUppercase = True
        #test if contains a number
        hasNumber = Validator.has_numbers(password)
        #write errors if something is wrong and return false, true otherwise
        if not(validLength):
            print("The length of the password is wrong, must be between 3 and 15 characters. Your has", len(password), "characters")
        if not(hasLowercase):
            print("The password must contain at least 1 lowercase letter")
        if not(hasUppercase):
            print("The password must contain at least 1 uppercase letter")
        if not(hasNumber):
            print("The password must contain at least 1 number")
        if(validLength and hasLowercase and hasUppercase and hasNumber):
            return True
        else:
            return False
    
    #test if the username meets the criteria, is used in the registration process
    #returns true if the username is valid, false otherwise and prints the corresponding error message
    def isVaildUsername(self, username):
        #between 3 and 15 characters, all characters allowed, else write error message and return false
        DAO = SQLQuerries()        
        length = len(username)
        if (length <3):
            print("The username is to short, must be at least 3 characters")
            return False
        elif (length>15):
            print("The username is to long, maximum 15 characters allowed")
            return False      
        #database querry if username is already taken
        usernameTaken=(DAO.usernameExists(username))
        if(usernameTaken):
            return True
        else:
            return False
    
    #test if value is in list of other values. used for selection of id if it is in the list of valid id'd to choose from
    #returns true if the is is in the list(valid), false otherwise
    def isInList(self, value, ListOfId):
        
        try:
            tmp = int(value)
            if(tmp in ListOfId):
                return True
            else:
                print("Input must be a valid id")
                return False
        except:
            print('The input must be a number')
            return False
        



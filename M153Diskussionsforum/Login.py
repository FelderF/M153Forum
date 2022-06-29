from Validator import Validator
from sqlQuerries import SQLQuerries


#used for the login and registration prozess
#create used objects, DAO for database acces, validator to validate inputs
DAO = SQLQuerries()
Validator = Validator()

#login function for regular login and admin login mask.
#Takes inputs from the user and checks, if they are valid. Then passes the values to the DAO if neccesarry

#takes input from the user and validates with the external validator. If input is invalid, asks again and prints the coresponding error
#if all the inputs are plausible, passes the parameters to the DAO for the database stuff
#DAO returns the userId if the login data matches, 0 otherwise. Because phython interprets bool test of integers 0 as false, and everything as true, this can be used in further statements.
#the user id is often used in the rest of the programm, with this method, only one database access is needed for the login and the retrieving of the userId
def login(admin = False):
    #take data for the login from the user, input must be repeated until an input is given for username and password. This is validated in the Validator class
    print("Please enter your username:")
    username = input()
    while not (Validator.isNotEmpty(username)):
        print("The username cannot be emptry, please enter your username again")
        username = input()
    print("Please enter your password:")
    password = input()
    while not (Validator.isNotEmpty(password)):
        print("The password cannot be emptry, please enter your username again")
        password = input()
    #database query if username and password matches, returns 0 if no match was found, the userId otherwise.
    #Because duplicate usernames are not allowed, ths function returns a distinct userId
    #If the parameter admin=true is passed, it also tests if the user who tries to login is an admin as well
    return(DAO.testLogin(username, password, admin))

#used for the admin login, passes the parameter admin=true to the login function. This is used in the login function to determine if a test if the user is an admin is neccessarry. 
# Passes the user id to the main function if admin login was succesfull, false otherwise
def adminLogin():
    LoginSuccesfull = login(True)
    if(LoginSuccesfull):
        print("Login succesfull")
        return LoginSuccesfull
    else:
        print("login falied")
        return False

#used for registration of new users
#tests first if the input is valid with the external Validator, repeats input otherwise
#username must be unique and between 3 and 15 characters, password mus be between 12 and 99 characters, contain 1uppercase, 1lowercase and 1number to be valid
#also tests if the username is not already in use, repeats input otherwise
def registration():
    print("Please enter your desired username. Must be between 3 and 15 characters and not already in user")
    username = input()
    #tests if username is valid and not already in use, else the function prints the error message and repeats input
    while not Validator.isVaildUsername(username):
        print("Please enter your desired username again.")
        username = input()
    #tests if password matches criteria, repeats input otherwise
    print("Please enter a password. It must be at leas 12 characters (maximum 99), contain at lease one lowercase letter, one uppercase and one number")
    password = input()
    while not Validator.isValidPassword(password):
        print("Please enter your password again")
        password = input()
    #call DAO to insert new user credentials
    DAO.insertNewUser(username, password)
    #returns true just for fun
    return True



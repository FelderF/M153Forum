from Validator import Validator


def login(admin = False):
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
    #database query if username and password matches
    #if admin == True, additional test if the user is an admin
    #return true if login succesfull, false otherwise
    return True

def adminLogin():
    LoginSuccesfull = login(True)
    return LoginSuccesfull

def registration():
    print("Please enter your desired username. Must be between 3 and 15 characters and not already in user")
    username = input()
    while not Validator.isVaildUsername(username):  #tests if username is valid and not already in use, else the function prints the error message
        print("Please enter your desired username again.")
        username = input()
    print("Please enter a password. It must be at leas 12 characters (maximum 99), contain at lease one lowercase letter, one uppercase and one number")
    password = input()
    while not Validator.isValidPassword(password):
        print("Please enter your password again")
        password = input()
    #call DAO to insert new user credentials
    return True

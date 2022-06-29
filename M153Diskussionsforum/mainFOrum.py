from Login import login
from Login import registration
from Login import adminLogin
from connectExt import connect

#Start
#while not want to quit, do the following loop
#test if logged in, if no, call login, else continue
#if logged in, select eighter category management or user management
#port 5432

if __name__ == '__main__':
    connect()
connect()
print("welcome to the forum")
loggedIn = bool(False)
ToDo ="n"
while ToDo != "e":
    print("Please choose what you want to do:")
    print("l - Login to the forum")
    print("r - Registration")
    print("i - initialize database")
    print("a - admin section")
    print("e - exit")
    ToDo = input()
    if ToDo == "l":
        #call login function
        isLoggedIn = login()    #returns true if login was succesfull, otherwise false
        if isLoggedIn:
            print("You are now logged in")
            #Call the category function
    elif ToDo == "r":
        #call registration function
        #returns true if registration was succesfull, false otherwise
        if registration():
            print("you are now registred, welcome!")
        else:
            print("Something went wrong, sorry!")
    elif ToDo =="i":
        #call database initializer function without return value
        pass
    elif ToDo =="a":
        isLoggedIn = adminLogin()
        if isLoggedIn:
            pass
        #call admin function, without return value
        pass
    elif ToDo == "e":
        #skipp the while loop and exit afterwards
    else:
        print("Please enter a valid input")
print("goodbye")

    
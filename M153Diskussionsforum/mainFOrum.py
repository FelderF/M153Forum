from re import A, I, L
from urllib.parse import parse_qsl
from Login import login
from Login import registration
from Login import adminLogin
from Validator import Validator
from initalizeDB import initializeDB
from sqlQuerries import SQLQuerries
import psycopg2
import os

#Start
#programm starts here, controls a forum with categories, topics and posts
#first choose what to to: set up the database with all the needed tabels and sample data
#login with username and password
#register a new regular user
#enter the admin section with username password for an admin account
#programm can be exited or get one step back with e
#sample user credentials: 
# user1, Password12345      regular user with sample posts
# user2, Password54321      regular user with sample posts
# admin, Adminpassword12345 admin user
#

print("welcome to the forum")
#create used objects for database acces and Validation
DAO = SQLQuerries()
Validator = Validator()
#set control variables to default values
userID = "0"
ToDo ="n"
while ToDo != "e":

#Main Menue
    print("Please choose what you want to do:")             
    print("l - Login to the forum")                     #login as regular user with username password, available for all users
                                                        #allows see all categories, see topics for categories, posting in topic, alter/delete own posts, change own username
    print("r - Registration")                           #create new user with username password, generated as regular user(no admin)
    print("i - initialize database")                    #create needed tables in db(credentials are stored in databese.ini and can be adjusted for own database) and fills it with sample data
    print("a - admin section")                          #acces to admin section, only for admin acoounts, allows changin of user roles(admin/user), delete users, see all users, create new topic, create new category, look for users
    print("e - exit")                                   #exit forum
    ToDo = input()
    if ToDo == "l":
        #call login function, takes credentials from the user and tests if password and username matches
        #returns 0 if loggin falied, else returns the userID if login was succesfull, otherwise false, userId is used often later in the programm
        userID = login()   

#regular user Area
        if userID:            
            selection=""
            if(selection==""):
                print("Input was wrong, please try again")    
            _ = os.system('cls')        
            print("You are now logged in")
            print("Select what to do next")
            while(selection !="1") or (selection !=2) or (selection !=3):
                print("1 - show categories (allows posting)")           #list all categories, deeper down in this section posts can be created
                print("2 - see own posts (allows editing)")             #lists all own posts, allows editing and deleting them
                print("3 - log out (allows switchig accout)")           #drop userid and return to the main menue
                print("4 - change username")
                selection = input()

    #user sees categories
                #here the users sees all the categories and can choose one by id to see the topics of the category, can be exited with e
                if (selection == "1"):
                    _ = os.system('cls')
                    #list all categories with name and id, an id can be selected to show all of its topics, returns a list with all the id's of the available categoties for further use
                    listOfId = DAO.printAllCategories()             
                    print("To select a category, insert the id, enter e to exit")
                    categoryId = input()                                       
                    #test if the choosen id is an id of an existing categories, else repeats input
                    while(categoryId != "e") and (not Validator.isInList(categoryId, listOfId)):        
                        print("please try again")
                        categoryId = input()
                    _ = os.system('cls')

    #user sees topics of single category, choosen by id
                    if(categoryId != "e"):
                            #show the name of the choosen category
                            DAO.printCategoryName(categoryId)
                            #list all the topics of the choosen category, returns a list of all the id's of the listed topics for further use
                            listOfTopicId = DAO.TopicsOfCategory(categoryId)
                            #user can select a topic by id to see all posts in that topic, id is tested if it is in the valid list
                            print("To select a topic, enter the id, enter e to exit")
                            topicId = input() 
                            while(topicId !="e") and (not Validator.isInList(topicId, listOfTopicId) ):
                                topicId=input()

    #user sees all posts of a single topic
                            if(topicId != "e"):
                                #print list of all posts of the choosen topic
                                DAO.PostsOfTopic(topicId)
                                #y--> create a post
                                #n--> get back one step, to topic list
                                print("Do you want to add a post (y/n)?")
                                newPost = input()
                                if(newPost=="y"):
                                    #take input from user for new post, a title and text is needed, only validated if not empty
                                    print("empty inputs lead to a repetition of the mask")
                                    title=""
                                    text=""
                                    while(not title):
                                        print("Please enter a title for the post")
                                        title =input()
                                    while(not text):                                        
                                        print("Please enter a text for the post:")
                                        text = input()    
                                    #new post is created, with the logged in users id and the selected topic id        
                                    DAO.createNewPost(topicId, userID, title, text)                
                    _ = os.system('cls')   

    #users sees all of its own posts
                elif (selection =="2"):
                    _ = os.system('cls')
                    print("Your own post")
                    #lists all the posts of the logged in user, sorted by topic name, returns a list with the id of the users posts id's
                    listOfPostId = DAO.ShownOwnPosts(userID)
                    #user can select an own post by id for editing
                    print("To edit a post, please enter the id, enter e to exit")
                    postID = input()                    
                    #choosen post id must be one of his own posts
                    while(postID !="e") and (not Validator.isInList(postID, listOfPostId) ):
                        postID=input()
    #user can edit own post
                    if(postID != "e"):
                        print("Press d to delete")                  #delete selected post
                        print("Press u to edit the text")           #alter the text of the selected post
                        print("Press e to exit")                    #return 
                        selection = input()

                        #delete selected post without further confirmation from the user
                        if(selection == "d"):
                            DAO.deletePost(postID)
                            print("Post deleted")

                        #takes input to change text of the post and alters it in db
                        elif(selection == "u"):
                            print("what sould the new text be?")
                            #if the input is empty, user is returned because his fault
                            newTitle = input()
                            #if desired new text has something in it, text of post is changed, based on the previous selected postId
                            if(Validator.isNotEmpty(newTitle)):
                                DAO.updatePost(postID, newTitle)
                                print("Post updated")
                            #if the user fails to enter an input, he is sent back to start to try again
                            else:
                                print("The text cannot be empty, back to start")
                        #user wants to exit
                        elif(selection != "e"):
                            print("Something went wrong, back to start")

    #user changes own username
                elif(selection =="4"):
                    #takes input for new username, must fulfill same criteria as in registration
                    print("Please enter your new username:")
                    newusername = input()
                    while not Validator.isVaildUsername(newusername):
                        print("Please enter your desired username again.")
                        username = input()
                    #if username is valid an not already taken, the name is updated in the db
                    DAO.changeUsername(userID, newusername)

    #user logs out of the forum, to eigther close or select new option/user account
                elif (selection == "3"):
                    #reset selection variables to default
                    userID=""
                    ToDo="n"
                    _ = os.system('cls')
                    print("logging out")
                    break
                else:
                    _ = os.system('cls')

#registration of new user
    elif ToDo == "r":
        #call registration function
        #returns true if registration was succesfull, false otherwise
        if registration():
            _ = os.system('cls')
            print("you are now registred, welcome!")
        else:
            print("Something went wrong, sorry!")

#initialize database with tables and sample data
    elif ToDo =="i":
        #call database initializer function without return value, sets up tables and fills with sample data
        initializeDB()

#admin area
    elif ToDo =="a":
        #call loginfunction with adminparameter, extenden login with test if the user has the admin role
        userID = adminLogin()
        if userID:
            _ = os.system('cls')
            print("Welcome admin")
            #prints a full list of all the users in the forum, returns a list of all the id's of the users for further selection
            print("Here is a full list of all the users with theire status")
            listOfUserId=DAO.printAllUsers()
            select = ""

            while(select != "a")and(select !="u")and(select!="d")and(select!="e"):                           
                while(select!="e"):
                    print("Please select what to do")
                    print("a - promote user to admin")              #change userrole to admin
                    print("u - degrade user to regular user")       #change userrole to regular user       
                    print("d - delete User")                        #delete user, selected by id
                    print("c - create new category")                #creation of new category in the forum
                    print("t - create new topic")                   #create a new topic an assign to category
                    print("l - look for user by name")              #look for user by name in the db, returns the id(can be used to change privileges of user)
                    print("e - exit admin area")     
                    select = input()

    #admin promotes user to admin
                    if(select=="a"):
                        #takes id as input and tests, if is id of an existing user. Doesn't test if the user is already an admin
                        print("Please enter the id of the user to promote to admin")
                        userId = input()
                        while( not Validator.isInList(userID, listOfUserId)):
                            print("Please enter a valid id")
                            userID = input()
                        #if a existing user id is selected, it changes his roleId to 1, this assigns the role of admin to that user
                        DAO.promoteUser(userId, 1)    

    #admin degrades user to regular user                
                    elif(select=="u"):
                        #takes id as input and tests, if is id of an existing user. Doesn't test if the user is already a regular user and if he is the last admin(can break the forum becasue an admin is needed for certian actions)
                        print("Please enter the id of the user to promote to user")
                        userId = input()                        
                        while( not Validator.isInList(userID, listOfUserId)):
                            print("Please enter a valid id")
                            userID = input()
                        #if a existing user id is selected, it changes his roleId to 2, this assigns the role of regular user to that user
                        DAO.promoteUser(userId, 2) 

    #admin looks up user
                    elif(select=="l"):
                        #enters username to get id of the user
                        print("please enter the username to get the corresponding userid") 
                        usernameToLookup = input()    
                        while (not usernameToLookup):
                            print("Please enter the username again.")
                            usernameToLookup = input()    
                        #looks in the db if a user with exactly that username exists, prints the users id if yes, prints an error if no user was found
                        DAO.userLookup(usernameToLookup)

    #admin delets user
                    elif(select=="d"):
                        #takes id of existing user as input, test if it is an existing user
                        print("Please enter the id of the user to delete")
                        userId = input()
                        while( not Validator.isInList(userID, listOfUserId)):
                            print("Please enter a valid id")
                            userID = input()
                        #deletes user from db
                        DAO.deleteUser(userId)    
    
    #admin creates new category
                    elif(select=="c"):
                        #admin enters a name for a category, because admins are skilled users and know whath they do, no validation is done and no test if the category already exists
                        print("Please enter the name of the new category")
                        newCategory = input()
                        DAO.createNewCategory(newCategory)

    #admin creates new topic
                    elif(select=="t"):
                        #admin enters a name for a new topic and assigns it to a category by id
                        #because admins are often geniouses, no furter evaluation is done and the category is assigned by giving the desired category id
                        print("Please enter the name for the new topic")
                        newTopic = input()
                        print("Please enter the categoryId")
                        newTopicCategoryId = input()
                        DAO.createNewTopic(newTopicCategoryId, newTopic)
    
    #admin logout
                    elif(select=="e"):
                        #reset selection variables to default
                        userID=""
                        ToDo="n"
                        print("logout of admin area")
                    else:
                        print("Invalid input, try again")                
        
    elif ToDo == "e":
        #skipp the while loop and exit afterwards        
        pass
    else:
        #if the user didn't enter a valid option
        print("Please enter a valid input")

#exit the programm while crying a little bit because you already miss it
print("goodbye")

    
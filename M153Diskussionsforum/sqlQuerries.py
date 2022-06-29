
from re import T
from config import config
import psycopg2

#different sql querries for the database acces, takes inputs from the main function or others.
#creates connection with parameters from the config file, executes statement and some return values like the list of valid id's or the selected data from a select statement
#validity of the input is testes in the main function

class SQLQuerries():   
    #prints all users stored in the db, orderd by name. returns a list with all the id's of the users for further functions
    def printAllUsers(self):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            #prepare sql
            sqlqry = """SELECT * FROM users ORDER BY name ASC"""
            cur.execute(sqlqry)
            #print data and append id of the users to list for the return
            print("id\trole\tusername\tpassword")
            users = cur.fetchall()
            listOfUserId = []
            for row in users:
                print(row[0],"\t",row[1],"\t",row[2],"\t\t",row[3])
                listOfUserId.append(row[0])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
            #returns the list with the id's
            return(listOfUserId)

    #prints all the categories in the db, returns a list with all the id's of the categories for other functions
    def printAllCategories(self):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = """SELECT * FROM category"""
            cur.execute(sqlqry)
            ListOfCategories = cur.fetchall()
            ListOfCategoryId = []
            #print all data and store id in list
            print("Id\tname")
            for row in ListOfCategories:
                print(row[0],"\t",row[1])
                ListOfCategoryId.append(row[0])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
            #returns list with id's to the main function
            return(ListOfCategoryId)

    #prints all the topics of a specific category, needs a valid category id, this is checked beforehand
    #returns a list with all the topic id's of the category for other functions
    def TopicsOfCategory(self, categoryID):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT * FROM topic WHERE categoryid = %s"
            cur.execute(sqlqry,(categoryID,))
            posts = cur.fetchall()
            print("Topics:\nId\tname")
            ListOfTopicsId = []
            #print data and store id's in list
            for row in posts:
                print(row[0],"\t",row[2])
                ListOfTopicsId.append(row[0])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
            #return list of id's
            return(ListOfTopicsId)

    #prints all the topics with the corresponding categoryid of the assigned category, returns nothing
    #is not used in the program
    def TopicsWithCategory(self, categoryID):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT * FROM topic WHERE categoryid = %s"
            cur.execute(sqlqry,(categoryID,))
            posts = cur.fetchall()
            #print all the data
            for row in posts:
                print("Id = ", row[0],)
                print("name = ", row[2],)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
    
    #lists all posts of a specific topic with the name of the user who created it, oders them by the timestamp(is generated automatically in the creation of the posts)
    #needs the topicid from main
    #return value is not used, but created if ever needed
    def PostsOfTopic(self, topicId):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT post.name, post.text, users.name FROM post INNER JOIN users ON post.userid=users.id WHERE topicid = %s ORDER BY timestamp ASC"
            cur.execute(sqlqry,(topicId,))
            posts = cur.fetchall()
            #print all the posts of the topic and stores id in list
            print("Posts:\n")
            ListOfPostsId = []
            for row in posts:
                print(row[0],"\n",row[1],"\nby ",row[2],"\n")
                print("-----------------")
                ListOfPostsId.append(row[0])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
            #return list of ids of corresponding posts, is never used in other functions
            return(ListOfPostsId)

    #show all posts of the desired user, needs the userID, which is stored when the user loggs in
    #returns a list with id's of all the users posts, used for editing these/deleting afterwards
    def ShownOwnPosts(self, userID):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT post.id, topic.name, post.name, post.timestamp, post.text FROM post INNER JOIN topic ON post.topicid = topic.id WHERE userid = %s ORDER BY topic.name ASC"
            cur.execute(sqlqry,(userID,))
            posts = cur.fetchall()
            #print all posts and store id's
            print("Id\ttopic\t\tname\t\t\ttimestamp\ttext")
            listOfPostId = []
            for row in posts:
                print(row[0],"\t",row[1],"\t\t",row[2],"\t\t",row[3])
                listOfPostId.append(row[0])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')
            #return id's to main for other functions
            return listOfPostId

    #tests if username and password matches
    #can also test if the user is an admin or not
    #needs username and password, and optional if test for admin status is desired
    #returns true if data match(username/password combination and if desired admin status), false otherwise
    def testLogin(self, username, password, isAdmin= False):
        user = None
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            #lookup if a user with this name exists, because username is unique by registration rules, only one is needed in the further process
            sqlqry = "SELECT * FROM users WHERE name = %s"
            cur.execute(sqlqry,(username,))
            user = cur.fetchone()            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')    
        #is executed if no user was found because the string user is then empty(sql select returns nothing)   
        if(not user):
            print("no user found")
            return False
        #test if the given password matches with the one of the user stored in the db, returns false if they dont match
        elif(user[3]!= password):
                return False
        #if desired, an admintest is done aswell, test if the userrole ID is 1(the one of the admin role because the db was setup that way int he initializin process)
        #if everything is fine, returns the user id for other functions
        elif(isAdmin):
            if(user[1]==1):
                return user[0]
            else:
                return False
        #if everything matches, returns the userid for later use
        else:
            return user[0]       

    #deletes post with the given postID from the db
    def deletePost(self, postId):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "DELETE FROM post WHERE id = %s"
            cur.execute(sqlqry,(postId,))            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')            
        

    #change post title, needs the post id and the new title
    #if id is valid and title is not empty is testet in the main function
    def updatePost(self, postId, newTitle):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "UPDATE post SET text = %s WHERE id = %s"
            cur.execute(sqlqry,(newTitle, postId,))            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')    

    #tests if the username already exists, if so prints an error and returns false, returns true otherwise. 
    #Because usernames are unique, fetchone can be used
    def usernameExists(self, username):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT * FROM users WHERE name LIKE %s"
            cur.execute(sqlqry,(username,))  
            oneExistingUser = cur.fetchone()    
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
            if(oneExistingUser):
                print("username already taken")
                return False
            else:
                return True
                #print('Database connection closed')   
        

    #inserts new ueser in db with desired username and password. New vreated users are assigned the user role. Validation is done beforehand
    def insertNewUser(self, username, password):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "INSERT INTO users(name, password, roleid) VALUES(%s, %s, 2)"
            cur.execute(sqlqry,(username,password,))   
            print("here)")           
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')   
            return True

    #change userrole to regular user or admin, needs the user id and the new roleid(1 for admin, 2 for regular user)
    #is only called by admins
    def promoteUser(self, id, roleid):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "UPDATE users SET roleid = %s WHERE id = %s"
            cur.execute(sqlqry,(roleid, id,))            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')  
    
    #delete user from db according to given id, is called by admins
    def deleteUser(self, id):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "DELETE FROM users WHERE id = %s"
            cur.execute(sqlqry,(id,))            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    #prints name of the choosen category by id for display purpose, is used in lsiting of all the topics 
    def printCategoryName(self, categoryId):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT name FROM category WHERE id = %s"
            cur.execute(sqlqry,(categoryId,))       
            name = cur.fetchone()
            print("Category:")
            print(name[0],"\n")     
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    #users can create new posts, needs the userid, topicid to assign to, desired name and text of post. Validation is tested in main
    def createNewPost(self, topicId, userId, name, text):
        try:
            params = config()
            print("here")
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "INSERT INTO post(topicid, userid, name, text) VALUES(%s,%s,%s,%s)"
            cur.execute(sqlqry,(topicId,userId, name, text,)) 
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    #admins can create new categories, just needs the desired name
    def createNewCategory(self, categoryName):
        try:
            params = config()
            print("here")
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "INSERT INTO category(name) VALUES(%s)"
            cur.execute(sqlqry,(categoryName,)) 
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    #admins can create new topics, needs categoryid to assign to and desired name
    def createNewTopic(self, categoryId, topicName):
        try:
            params = config()
            print("here")
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "INSERT INTO topic(categoryid, name) VALUES(%s,%s)"
            cur.execute(sqlqry,(categoryId, topicName,)) 
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    #changes username in db, needs userid and desired new username
    #users can change theire own username
    #test if username is not already taken an is valid is done in the main
    def changeUsername(self, userId, username):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "UPDATE users SET name = %s WHERE id = %s"
            cur.execute(sqlqry,(username, userId,))            
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection closed')  
    
    #used to find userid by username, used by admins, only matches equal strings, substrings don't result in a userif
    #because usernames are unique, fetchone can be used
    #prints the userid if one is found or prints an error message if none exists
    def userLookup(self, usernameToLookup):
        try:
            params = config()
            #connect to PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sqlqry = "SELECT id FROM users WHERE name like %s"
            cur.execute(sqlqry,(usernameToLookup,))       
            name = cur.fetchone()
            if(name):
                print("id of the user is:")
                print(name[0],"\n") 
            else:
                print("No user with this name exists") 
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
from config import config
import psycopg2
#Needed querys
#Login for users
#Login with parameter if is admin, can be similar with optional parameter
#Registration: test if username already exists
#Registration insert
#Look for user based on username
#List number of users
#Reset password, optional to given string
#delete user
#create user
#create/update/delete/read for:
#topic/category/thread
def connect(sqlqry=""):
    conn = None    
    try:
        params = config()
        #connect to PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sqlqry)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')
    pass

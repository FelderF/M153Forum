from config import config
import psycopg2
#used to initialize database with needed tables and sample values, gets the prepared sql statment from the initializeDB
def connect(sqlqry=""):
    conn = None    
    try:
        params = config()
        #connect to PostgreSQL server
        conn = psycopg2.connect(**params)
        #create cursor to execute passed sql statement
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

import psycopg2, sys
#not used, templaste for database connection
modulename = 'psycopg2'
if 'psycopg2' not in modulename:
    print('Module not loaded')

def connect(self):
    try:
        conn = psycopg2.connect(host="localhost",
        database="forum",
        user="postgres",
        password="admin")
    except psycopg2.OperationalError as e:
        print('Unable to connect!\n')
        # log.error(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
        if conn: conn.rollback()
        print(e)
        sys.exit(1)
    else:
        print('Connected!')
'''
    conn = psycopg2.connect(
        host="localhost",
        database="forum",
        user="postgres",
        password="admin")
'''
#connect()

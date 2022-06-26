from ForumDAO import connect

def initializeDB():
    sqlqry = """CREATE TABLE images (
                IMG_ID                        SERIAL PRIMARY KEY,
                title                         VARCHAR(255), 
                description                   VARCHAR(255),
                image_file                    BYTEA 
            )"""                       
    connect(sqlqry)
    pass
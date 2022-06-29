from ForumDAO import connect
#used to prepare the database
#first creates needed tables, then inserts sample data with prepared users for access
def initializeDB():

    #create tables
    sqlqry = """CREATE TABLE users (
                ID                  SERIAL PRIMARY KEY,
                roleID              INTEGER, 
                name                VARCHAR(25),
                password            VARCHAR(100)
            );
            CREATE TABLE role (
                ID                  SERIAL PRIMARY KEY,
                name                VARCHAR(25), 
                description         VARCHAR(255)
            );
            CREATE TABLE category (
                ID                  SERIAL PRIMARY KEY,
                name                VARCHAR(255)                
            );
            CREATE TABLE topic (
                ID                  SERIAL PRIMARY KEY,
                categoryID          INTEGER, 
                name                VARCHAR(255)
            );
            CREATE TABLE post (
                ID                  SERIAL PRIMARY KEY,
                topicID             INTEGER, 
                userID              INTEGER, 
                name                VARCHAR(255),
                text                TEXT,
                timestamp           TIMESTAMP
            ); 
            ALTER TABLE post ALTER COLUMN timestamp SET DEFAULT now()            
            """
    #execute table generating
    connect(sqlqry)
    #call function to fill with sample data
    insertSample()

#insert sample data, creates 2 regular users, one admin and assigns the roles.
#creates different categories, topics and posts as examples
def insertSample():
    sqlqry = """
        INSERT INTO role(name, description) VALUES
        ('administrator','can change user data, can create categories' ),
        ('user','can post, create topics, modify own posts' );
        
        INSERT INTO users(roleid, name, password) VALUES
        (1, 'admin', 'Adminpassword12345' ),  
        (2, 'user1', 'Password12345' ),  
        (2, 'user2', 'Password54321' );  
        
        INSERT INTO category(name) VALUES
        ('Forum feedback' ),
        ('Off topic' );
        
        INSERT INTO topic(categoryid, name) VALUES(1, 'User Inerface' ),        
        (1, 'Members' ),  
        (2, 'Jokes' );
        
        INSERT INTO post(topicid, userid, name, text) VALUES
        (1, 2, 'good', 'the interface is fantastic, someone truly created art here!!!'),
        (1, 3, 'bad', 'How did this interface pass through the council of the internet? Theres no single cat picrute here?!?'), 
        (2, 2, 'user2', 'I love user 2, hes so lovely'),
        (2, 3, 'user1', 'Why is user1 here? Hes stalking me all over the internet'),
        (3, 2, 'knock knock', 'Knock knock!'),
        (3, 2, 'whos there', 'Whos there?'),
        (3, 2, '******', 'comment deletet because it was not funny enough'),
        (3, 3, 'Anybody here', 'Has nobody some good jokes to share? I would start, but my jokes are to complex for you to understand');
    """
    connect(sqlqry)
from dbConnectionEstablisher import getDbConnection, dbConfig
from dotenv import load_dotenv, set_key
import os


load_dotenv()
usersTable = os.getenv("DB_TABLE")


# ======
# fetching data
# ======

#  get data from db
def getAllData(*args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable}')
    data = cursor.fetchall()
    connection.close()
    return data


#  search for a user by name - partly or fully match
def searchUserName(name, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable} WHERE lower(userName) like lower(%s)', (f'%{name}%',))
    data = cursor.fetchall()
    connection.close()
    return data


#  search for a user by mail - partly or fully match
def searchUserMail(mailAddress, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable} WHERE lower(mail) like lower(%s)', (f'%{mailAddress}%',))
    data = cursor.fetchall()
    connection.close()
    return data


#  search for a user by name -  full match
def searchUserNameFM(name, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable} WHERE lower(userName) = lower(%s)', (name,))
    data = cursor.fetchall()
    connection.close()
    return data


#  search for a user by mail -  full match
def searchUserMailFM(mailAddress, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable} WHERE lower(mail) = lower(%s)', (mailAddress,))
    data = cursor.fetchall()
    connection.close()
    return data

    
#  get data from db according to user dynamic id
def fetchUser(id, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {usersTable} WHERE userNum = %s', (id,))
    data = cursor.fetchall()
    connection.close()
    
    return data[0]


# ======
# DB operations
# ======

#  create DB as the name configured in .env - only if not exist
def createDB(*args):
    if args[0] != None:
        dbName = args[0]
    else:    
        dbName = "webpageusers"
    global usersTable
    usersTable = os.getenv("DB_TABLE")
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    sqlQueries = [f"create database if not exists {dbName};",
                    f"use {dbName};",
                  f""]
    
    for query in sqlQueries:
        cursor.execute(query)
        print(query)
    
    connection.commit()
    cursor.close()
    connection.close()

    global dbConfig
    dbConfig['database'] = dbName
    usersTable = os.getenv("DB_TABLE")

    print(dbConfig['database'])
    set_key('.env', 'DB_NAME', dbName)

    load_dotenv()
    
    isExist = isExistTable(dbName, usersTable)
    if isExist == 0:
        createDbTable(dbName)
    
    return print("Done createDB")


# check if table exist in database
def isExistTable(dbName, tableName):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select count(*) as count from information_schema.tables where table_schema = '{dbName}' and table_name = '{tableName}';")
    ans = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return ans['count']
    
    
#  re-arrange indices
def reArrangeIndices():
    tempTable = "tempForIndices"
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {os.getenv('DB_NAME')}.{tempTable}")
    cursor.execute(f"CREATE TABLE {os.getenv('DB_NAME')}.{tempTable} LIKE {usersTable}")
    cursor.execute("SET @id := 0")
    cursor.execute(f"INSERT INTO {os.getenv('DB_NAME')}.{tempTable} (userNum, userName, mail, profilePicName, phone, gender) SELECT @id := @id + 1 AS new_id, userName, mail, profilePicName, phone, gender FROM {usersTable} ORDER BY userNum")
    cursor.execute(f"DROP TABLE {usersTable}")
    cursor.execute(f"RENAME TABLE {os.getenv('DB_NAME')}.{tempTable} TO {usersTable}")    
    connection.commit()
    connection.close()


# create table for database
def createDbTable(db):
    usersTable = os.getenv("DB_TABLE")
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    sqlQueries = [
        f"DROP TABLE IF EXISTS {db}.{usersTable};",
        f"""CREATE TABLE {db}.{usersTable} 
            (
                userNum INT AUTO_INCREMENT PRIMARY KEY,
                userName VARCHAR(50),
                profilePicName VARCHAR(50),
                mail VARCHAR(50),
                phone VARCHAR(50),
                gender VARCHAR(6)
            );
            """
    ]

    for query in sqlQueries:
        cursor.execute(query)
        print(query)

    connection.commit()
    cursor.close()
    connection.close()


#  create the basic database
def createBasicDB(*args):
    createDbTable(os.getenv('DB_NAME'))
    connection = getDbConnection()
    cursor = connection.cursor()
    
    sqlQueries = [
        f"""
        INSERT INTO {os.getenv('DB_NAME')}.{usersTable} (userNum, userName, profilePicName, mail,  phone, gender)
        VALUES 
            (1, 'Peter Griffin', 'PeterGriffin.png', 'petergriffin@familyGuy.com', '+972505123456', 'Male'),
            (2, 'Stewie Griffin', 'StewieGriffin.png', 'stewiegriffin@familyGuy.com', '+972505123457', 'Female'),
            (3, 'Brian', 'Brian.png', 'brian@familyGuy.com', '+972505123458', 'Male');
        """
        ]
    
    for query in sqlQueries:
        cursor.execute(query)
        
    connection.commit()
    cursor.close()
    connection.close()
    

# ======
# Editing users
# ======

#  delete a user (full row) and re-arrange the indices
def dropUser(id, *args):
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM {usersTable} WHERE userNum = %s', (id,))
    deletedRowsCnt = cursor.rowcount
    connection.commit()
    connection.close()
    reArrangeIndices()
    return deletedRowsCnt


#  add a new user to the table
def addUser(user, *args):    
    connection = getDbConnection()
    cursor = connection.cursor()
    sqlQuery = f"""
        INSERT INTO {os.getenv('DB_NAME')}.{usersTable} (userName, mail, profilePicName, phone, gender)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(sqlQuery, (user['userName'], user['mail'], user['profilePicName'], user['phone'], user['gender']))
    connection.commit()
    cursor.close()
    connection.close()


    
#  Edit contact
def editUser(user, *args):
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    
    sqlQuery = f"""
        UPDATE {usersTable} SET userName = %s, mail = %s, 
        profilePicName = %s, phone = %s, gender = %s
        WHERE userNum = %s;
    """
    
    #  to prevent user from sending db commands within the query, pass as tuple
    cursor.execute(sqlQuery, (user['userName'], user['mail'], user['profilePicName'], user['phone'], user['gender'], user["_id"]))
    
    connection.commit()
    cursor.close()
    connection.close()

    
# ======
# fake Generator
# ======

# main operations to create fake db for first time
def performFakeOps(data, db):
    # global usersTable
    # usersTable = "fakeTable"
    createFakeDB(db)
    createBaseFakeDB(data, db)
    return getAllData(db)


#  create fake DB as the name configured in .env - only if not exist
def createFakeDB(db):
    dbName = db
    connection = getDbConnection()
    cursor = connection.cursor(dictionary=True)
    sqlQueries = [f"create database if not exists {dbName}",
                    f"use {dbName}"]
    
    for query in sqlQueries:
        cursor.execute(query)
        print(query)
    
    connection.commit()
    cursor.close()
    connection.close()
    global dbConfig, usersTable
    dbConfig['database'] = dbName
    usersTable = os.getenv(f'{dbName}_COL')
    print(dbConfig['database'])
    set_key('.env', 'DB_NAME', dbName)
    load_dotenv()
    return print("Done createDB")
    
    
#  create the basic fake database
def createBaseFakeDB(list, db):
    connection = getDbConnection()
    cursor = connection.cursor()
    
    sqlQueries = [
        f'DROP TABLE IF EXISTS {db}.{usersTable};',
        f"""CREATE TABLE {db}.{usersTable} (
            userNum INT AUTO_INCREMENT PRIMARY KEY,
            userName VARCHAR(50),
            profilePicName VARCHAR(50),
            mail VARCHAR(50),
            phone VARCHAR(50),
            gender VARCHAR(6)
        );
        """
        ]
    for user in list:
        query = f"""
        INSERT INTO {db}.{usersTable} ( userName, profilePicName, mail,  phone, gender)
        VALUES ('{user['userName']}', '{user['profilePicName']}', '{user['mail']}', '{user['phone']}', '{user['gender']}');
        """
        sqlQueries.append(query)
    
    for query in sqlQueries:
        cursor.execute(query)
        
    connection.commit()
    cursor.close()
    connection.close()
    
    
# retrieve all data for fake table
def getAllFake(db):
    if db == "FAKE":
        createFakeDB(db)
        return getAllData(db)

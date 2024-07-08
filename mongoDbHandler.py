from dbConnectionEstablisher import getMongoConnection
import os


def createConnection(dbName):
    uri = os.getenv("MONGO_URI") + os.getenv(dbName)
    return getMongoConnection(uri)



# # ======
# # Fetching data
# # ======

# get data from db
def getAllData(db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    users = list(collection.find())
    return users
  
    
# search for a user by name - partly or fully match
def searchUserName(name, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    users = list(collection.find({"userName": {"$regex": f'.*{name}.*', "$options": "i"}}))
    return users


# search for a user by email - partly or fully match
def searchUserMail(email, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    users = list(collection.find({"mail": {"$regex": f'.*{email}.*', "$options": "i"}}))
    return users


# search for a user by name - fully match
def searchUserNameFM(name, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    users = list(collection.find({"userName": {"$regex": f'^{name}$', "$options": "i"}}))
    return users


# search for a user by email - fully match
def searchUserMailFM(mail, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    query = {"mail": {"$regex": f'^{mail}$', "$options": "i"}}
    users = list(collection.find(query))
    return users


#  get data from db according to user dynamic id
def fetchUser(id, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    user = collection.find_one({"_id": int(id)})
    return user


# ======
# DB operations
# ======

# create archive collection if not exists
def createDB(db):
    mongoDB = createConnection(db)
    col = os.getenv(f"{db}_COL")
    if col not in mongoDB.list_collection_names():
        mongoDB.create_collection(col)
    return "Collection is ready"


#  create the basic database
def createBasicDB(db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    collection.drop()
    mongoQuery = [
        {'_id': 1, 'userName': 'Peter Griffin', 'profilePicName': 'PeterGriffin.png', 'mail': 'petergriffin@familyGuy.com', 'phone': '+972505123456', 'gender': 'Male'},
        {'_id': 2, 'userName': 'Stewie Griffin', 'profilePicName': 'StewieGriffin.png', 'mail': 'stewiegriffin@familyGuy.com', 'phone': '+972505123457', 'gender':'Female'},
        {'_id': 3, 'userName': 'Brian', 'profilePicName': 'Brian.png', 'mail': 'brian@familyGuy.com', 'phone': '+972505123458', 'gender': 'Male'}]
    
    collection.insert_many(mongoQuery)
    

# function to get the last index in the collection - indices handling    
def getNextIndex(col):
    lastDoc = col.find_one(sort=[('_id',-1)])
    if lastDoc:
        return int(str(lastDoc['_id'])) + 1
    else:
        return 1


# function to manage indices dynamically
def reArrangeIndices(col):
    docs = list(col.find().sort('_id'))
    ind = 1
    for doc in docs:
        newDoc = doc.copy()
        newDoc['_id'] = ind
        col.delete_one({'_id': doc['_id']})
        col.insert_one(newDoc)
        ind += 1
  
  
# ======
# Editing users
# ======

# delete a user
def dropUser(id, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    result = collection.delete_one({"_id": int(id)})
    reArrangeIndices(collection)
    return result.deleted_count


# add a new archived user to the collection
def addUser(user, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    nextInd = getNextIndex(collection)
    user["_id"] = nextInd
    result = collection.insert_one(user)
    return str(result.inserted_id)


# edit an archived user
def editUser(user, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    ind = user["_id"]
    del user["_id"]
    result = collection.update_one(
        {"_id": int(ind)},
        {"$set": user}
    )
    return result.modified_count


# ======
# fake Generator
# ======

# main operations to create fake db for first time
def performFakeOps(data, db):
    createDB(db)
    createFakeDB(data, db)
    return getAllData(db)


# function to fill the database with documents
def createFakeDB(list, db):
    mongoDB = createConnection(db)
    collection = mongoDB[os.getenv(f"{db}_COL")]
    collection.drop()
    collection.insert_many(list)


# retrieve all data for fake table
def getAllFake(db):
    if db == "FAKE":
        createDB(db)
        return getAllData(db)    
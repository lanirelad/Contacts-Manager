from datetime import datetime
from flask import Flask, redirect, render_template, request
import os
import json
import fakerGenerator as fakeGen


#  create flask application
app = Flask(__name__)

# select case for db usage
def dbSwitch():
    global handler, archiveHandler, dbName
    if dataBaseSwitcher == "SQL":
        import mySqlHandler as handler
        import mongoDbHandler as archiveHandler
        dbName = None
    elif dataBaseSwitcher == "MONGO":
        import mongoDbHandler as handler
        dbName = "MANAGER"
        
        
#  declarations
imagesFolder = "static\\profileImages\\"
globalRowIndx = 0
emptyUserForEdit = {
    "_id": globalRowIndx,
    "userName": None,
    "profilePicName": None,
    "mail": None,
    "phone": "+0000000000000",
    "gender": None
    }
deletedImagesFolder = "static\\deletedImages\\"
dataBaseSwitcher = os.getenv("DB_USAGE")
archiveHandler = None
firstRun = True  # fake db first run
dbSwitch()


#  when page (table) loads
@app.route("/viewContacts")
def viewContacts():
    dbSwitch()
    global firstRun
    firstRun = True
    handler.createDB(dbName)
    # handler.createBasicDB(dbName) #  create the db with 3 initial characters
    data = handler.getAllData(dbName)
    return render_template("contactsMain.html", contacts=data)


#  remove contact from db
@app.route("/delete<rowNum>")
def deleteUser(rowNum):
    global dbName, dataBaseSwitcher, deletedImagesFolder, imagesFolder
    user = handler.fetchUser(rowNum, dbName)
    if user:
        userDict = dict(user)
        userDict["deleteStamp"] = datetime.now()
        
        if "userNum" in userDict:
            del userDict["userNum"]
        else:
            del userDict["_id"]

        # archive user data in MongoDB
        orgName = dbName
        dbName = "ARCHIVE"
        if archiveHandler:
            archiveHandler.addUser(userDict, dbName)
        else:
            handler.addUser(userDict, dbName)
        dbName = orgName

            
    # delete user from MySQL    
    success = handler.dropUser(rowNum, dbName)
    
    if success != 0:  
        
        print("successfully deleted")
        try:
            oldFile = os.path.join(imagesFolder, userDict["profilePicName"])
            newFile = os.path.join(deletedImagesFolder, userDict["profilePicName"])
            copyAndDelete(oldFile, newFile)
        except:
            print("error handling the images, or image not found!")
            
        
    if dbName == 'FAKE':
        return redirect('/fakeGen')
    else:    
        return redirect('/viewContacts')

    
#  opens the add contact form    
@app.route("/addContacts")
def addContacts():
    
    return render_template("addContact.html",invalid='False')


#  adding the new contact
@app.route("/addToContacts", methods=['POST'])
def postAddContact():
    phoneNum = request.form['phoneNumber']
    editedPhoneNum = "+972" + phoneNum
    contactName =request.form['contactName']
    mail = request.form['em']
    gender = request.form['gender']
    finalFileName = "None"
    profileImage = request.files['profileImg']

    if profileImage:  # store picture only if it submitted
        noSpacesName = contactName.replace(' ',"")
        finalFileName = noSpacesName + '.png'
        filePath = os.path.join(imagesFolder, finalFileName)
        profileImage.save(filePath)
    
    if handler.searchUserNameFM(contactName, dbName) or handler.searchUserMailFM(mail, dbName):
        ans = True
        return render_template("addContact.html",invalid=ans)
    else:
        
        userDict = {
            "userName": contactName,
            "profilePicName": finalFileName,
            "mail": mail,
            "phone": editedPhoneNum,
            "gender": gender
        }
        handler.addUser(userDict, dbName)
        if dbName == 'FAKE':
            return redirect('/fakeGen')
        else:    
            return redirect('/viewContacts')



#  editing a user    
@app.route("/edit<rowNum>")
def editContact(rowNum):
    global globalRowIndx
    global emptyUserForEdit
    if int(rowNum) == 0:
        globalRowIndx+=1
        data = emptyUserForEdit
    else:
        globalRowIndx = int(rowNum)    
        data = handler.fetchUser(rowNum, dbName)
    return render_template("editContact.html", contact=data, phoneNumber=data["phone"][4:])


#  submit changes from edit page
@app.route("/submitChanges", methods=['POST'])
def submitChanges():
    global globalRowIndx
    global imagesFolder
    orgCont = request.form['orgCont']
    phoneNum = request.form.get('phoneNumber')
    editedPhoneNum = "+972" + phoneNum
    contactName = request.form['contactName']
    mail = request.form['em']
    gender = request.form['gender']
    finalFileName = "None"
    profileImage = request.files['profileImg']

    if profileImage:  # store picture only if it submitted
        noSpacesName = contactName.replace(' ',"")
        finalFileName = noSpacesName + '.png'
        filePath = os.path.join(imagesFolder, finalFileName)
        profileImage.save(filePath)
    
    else:
        orgCont = orgCont.strip('"').replace("'", '"') 
        orgContDict = json.loads(orgCont)
        finalFileName = orgContDict["profilePicName"]
        filePath = os.path.join(imagesFolder, finalFileName)
        if orgContDict["userName"] != contactName and dbName != "FAKE":
            newFileName = os.path.join(imagesFolder, f"{contactName.replace(' ','')}.png")
            copyAndDelete(filePath, newFileName)
            finalFileName = f"{contactName.replace(' ','')}.png"

    userDict = {
            "_id": globalRowIndx,
            "userName": contactName,
            "profilePicName": finalFileName,
            "mail": mail,
            "phone": editedPhoneNum,
            "gender": gender
        }
    handler.editUser(userDict, dbName)

    if dbName == 'FAKE':
        return redirect('/fakeGen')
    else:    
        return redirect('/viewContacts')


#  filter table by searched name
@app.route("/search", methods=['POST'])
def searchByName():
    name = request.form.get('nameSearch')
    data = handler.searchUserName(name, dbName)
    
    if data and dbName == 'FAKE':  # results + fake search
        return render_template("contactsMain.html", contacts=data, fake = True)
    # elif data and dbName == "ARCHIVE":  # results + archive search
    #     return render_template("archivedContacts.html", contacts=data)
    elif data and dbName != 'FAKE':  # results + main page search
        return render_template("contactsMain.html", contacts=data)
    elif not data and dbName == 'FAKE':  # no results + fake search
        return redirect('/fakeGen')
    # elif not data and dbName == 'ARCHIVE':  # no results + archive search
    #     return redirect('/archive')
    else:
       return redirect('/viewContacts') 


# function to store deleted user's profile image and delete the origin    
def copyAndDelete(oldFile, newFile):

    # copy the image to the new location
    try:
        
        with open(oldFile, 'rb') as of:
            with open(newFile, 'wb') as nf:
                nf.write(of.read())
        
        # delete the original image
        os.remove(oldFile)
        
    except:
        print("error handling the images, or image not found!")        
    

# ======
# Archive
#=======

# show deleted contacts - mongoDB
@app.route("/archive")
def viewArchived():
    global dbName
    orgName = dbName
    dbName = "ARCHIVE"
    if archiveHandler:
        archiveHandler.createDB(dbName)
        data = archiveHandler.getAllData(dbName)
    else:
        handler.createDB(dbName)
        data = handler.getAllData(dbName)
    dbName = orgName
    return render_template("archivedContacts.html", contacts=data)
    

# search in archived contacts    
@app.route("/archiveSearch", methods=['POST'])
def searchArchivedByName():
    global dbName
    orgName = dbName
    dbName = "ARCHIVE"
    name = request.form.get('nameSearch')
    data = handler.searchUserName(name, dbName)
    dbName = orgName
    if data:
        return render_template("archivedContacts.html", contacts=data)
    else:
       return redirect('/viewContacts')


# ======
# Fake database
#=======
@app.route("/fakeGen")
def createFakedDB():
    global dbName, firstRun
    dbName = "FAKE"
    
    if firstRun:
        data = None
        firstRun = False
    else:
        data = handler.getAllFake(dbName)
    
    if data == None:
        size = 5
        fakeList = fakeGen.createFakeData(size)
        data = handler.performFakeOps(fakeList, dbName)    
    return render_template("contactsMain.html", contacts=data, fake = True)



if __name__ == "__main__":
    app.run(port=5056 ) #debug=True, 
    
    
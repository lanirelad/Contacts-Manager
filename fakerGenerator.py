import faker

# main function to create fake database in size of 'items'
def createFakeData(items):
    fakeGen = faker.Faker()
    users = []
    for i in range(items):
        gender = fakeGen.random_element(elements=('Male','Female'))
        if gender == 'Male':
            name = fakeGen.name_male()
        else:
            name = fakeGen.name_female()
            
        pic = f"https://robohash.org/{name.replace(' ', '')}.png"
        mail = fakeGen.email()
        pattern = "+972#########"
        phone = fakeGen.numerify(pattern)
        # print(name, mail, pic, phone, gender)
        users.append({
            "_id": i+1,
            "userName": name,
            "profilePicName": pic,
            "mail": mail,
            "phone": phone,
            "gender": gender
        })
        
    return users

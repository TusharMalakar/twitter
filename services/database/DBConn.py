from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://tweet:nKzHTG4VmIAHlKpz@twiter-pyyhe.mongodb.net/test?retryWrites=true&w=majority")
database = client.TWITER

# username = "testuser1@myhunter.cuny.edu"
# record = database.users.find_one({'username': username})
# print(record)

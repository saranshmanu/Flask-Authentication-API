from pymongo import MongoClient
import datetime

databaseLink = "mongodb://saransh.xyz"
name_of_the_database = "new_database"

# connect to the database
client = MongoClient(databaseLink)
# select the database to post the object
db = client[name_of_the_database]
posts = db.posts

print(posts)

post_many = [{
    "name":"Saransh Mittal",
    "date":datetime.datetime.now()
}, {
    "name":"Sky Blue",
    "date":datetime.datetime.now()
}]

post_one = {
    "name":"Saransh Mittal"
}

# returns array of the object id of the inserted objects
results = posts.insert_many(post_many)
# returns the object id of the inserted object
result = posts.insert_one(post_one)
# returns the total records in the database
total_objects = posts.count()

print(total_objects)
# returns the array of object ids returned after posting to the mongo database
posted_objects = results.inserted_ids
# returns the object id returned after posting to the mongo database
posted_object = result.inserted_id

print(posted_objects)
print(posted_object)

value = "Saransh Mittal"
# used to query the objects from the database
results = posts.find({"name": value})
for i in results:
    print(i)
# used to query a single object from the database
result = posts.find_one({"name": value})
print(result)
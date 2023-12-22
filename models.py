from mongoengine import *

username = "userweb17"
password = 321456
db = "WHW_8"
host = f"mongodb+srv://{username}:{password}@cluster0.r7yz0bl.mongodb.net/?retryWrites=true&w=majority"
connect(db=db, host=host)


class User(Document):
    completed = BooleanField(default=False)
    fullname = StringField(max_length=150)
    email = StringField(max_length=100)

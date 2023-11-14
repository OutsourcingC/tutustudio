from peewee import *
import hashlib

db = SqliteDatabase("database.db")

class Reservation(Model):
    date = DateField()
    name = CharField()
    last_name = CharField()
    phone = CharField()
    people = IntegerField()
    hour = TimeField()

    class Meta:
        database = db


class User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = 'users'


db.connect()
db.create_tables([Reservation])
db.create_tables([User])

if __name__ == '__main__':
    User.create(
        username='tutustudiobcn',
        password=hashlib.sha256(b'z13646885180').hexdigest()
    )


from peewee import *
import hashlib
import os

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))

db = SqliteDatabase(fr"{project_root}\database.db")

class Reservation(Model):
    date = DateField()
    name = CharField()
    last_name = CharField()
    phone = CharField()
    people = IntegerField()
    hour = TimeField()

    class Meta:
        database = db


class Users(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Reservation])
db.create_tables([Users])

if __name__ == '__main__':
    Users.create(
        username='tutustudiobcn',
        password=hashlib.sha256(b'z13646885180').hexdigest()
    )


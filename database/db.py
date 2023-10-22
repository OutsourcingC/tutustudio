from peewee import *

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


db.connect()
db.create_tables([Reservation])

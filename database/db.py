from peewee import *
import os

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))

os.makedirs(fr"{project_root}/database/db_files", exist_ok=True)
db = SqliteDatabase(fr"{project_root}/database/db_files/tutustudio_database.db")

class Reservation(Model):
    date = DateField()
    name = CharField()
    last_name = CharField()
    phone = CharField()
    people = IntegerField()
    reserve_hour = TimeField()
    reserve_time = TimeField()

    class Meta:
        database = db


db.connect()
db.create_tables([Reservation])

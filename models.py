from peewee import *

db = SqliteDatabase('database.db')

class Patient(Model):
    name = CharField()

    class Meta:
        database = db

class Doctor(Model):
    name = CharField()

    class Meta:
        database = db

class Visit(Model):
    visit_id = IntegerField()
    patient = ForeignKeyField(Patient, backref='visits')
    doctor = ForeignKeyField(Doctor, backref='visits')
    reason = CharField()
    duration = IntegerField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Patient, Doctor, Visit])

        #bruh machines
import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin, current_user
from peewee import *

DATABASE = SqliteDatabase('users_entries.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    title = CharField()
    date = DateTimeField()
    time = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, title, date, time, learned, resources):
        cls.create(
            title=title,
            date=date,
            time=time,
            learned=learned,
            resources=resources
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()


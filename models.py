"""Model classes for User and Entry"""
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin, current_user
from peewee import *

DATABASE = SqliteDatabase('users_entries.db')


class User(UserMixin, Model):
    """a subclass of Model that creates a user"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    )
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(UserMixin, Model):
    """Subclass of Model that creates entry """
    user = ForeignKeyField(model=User, backref='user')
    title = CharField()
    date = DateField()
    time = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    def get_entry(self):
        return Entry.select().where(Entry.user == self)

    @classmethod
    def create_entry(cls, user, title, date, time, learned, resources):
        cls.create(
            user=user,
            title=title,
            date=date,
            time=time,
            learned=learned,
            resources=resources,
        )

    @classmethod
    def edit_entry(cls, user, title, date, time, learned, resources):
        cls.update(
            user=user,
            title=title,
            date=date,
            time=time,
            learned=learned,
            resources=resources,
        )


def initialize():
    """Opens connection to database, creates table, and closes"""
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()


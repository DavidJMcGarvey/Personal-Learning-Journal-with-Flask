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

    def get_entry(self):
        """Gets entry"""
        return (
            User.select().join(
                Relationship, on=Relationship.cur_user
            ).wehre(
                Relationship.user_entry == self
            )
        )

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


class Entry(Model):
    """Subclass of Model that creates entry """
    user = ForeignKeyField(model=User, backref='entries')
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


class Relationship(Model):
    cur_user = ForeignKeyField(User, backref='user')
    user_entry = ForeignKeyField(Entry, backref='entry_of_user')

    class Meta:
        database = DATABASE
        indexes = (
            (('cur_user', 'user_entry'), True),
        )


def initialize():
    """Opens connection to database, creates table, and closes"""
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()


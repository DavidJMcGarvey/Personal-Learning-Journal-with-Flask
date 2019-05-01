"""Forms for Login, Registration, and Entry"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, DateField,
                     IntegerField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class EntryForm(FlaskForm):
    """FlaskForm for Entry information"""
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ])
    date = DateField(
        'Date (YYYY-MM-DD)',
        format='%Y-%m-%d',
        validators=[
            DataRequired()
        ])
    time = IntegerField(
        'Time (in minutes)',
        validators=[
            DataRequired()
        ])
    learned = TextAreaField(
        'Learned',
        validators=[
            DataRequired()
        ])
    resources = TextAreaField(
        'Resources',
        validators=[
            DataRequired()
        ])


class RegisterForm(FlaskForm):
    """FlaskForm for Registration information"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only")),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=7),
            EqualTo('password2', message='Password must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ])


class LoginForm(FlaskForm):
    """FlaskForm for Login information"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ])


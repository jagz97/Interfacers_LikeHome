from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, SubmitField, StringField, IntegerField, TextAreaField, SelectField, PasswordField, \
    BooleanField, validators, EmailField

# Set your classes here.


class RegisterForm(FlaskForm):
    name = StringField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = EmailField(
        'Email', validators=[DataRequired(),Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ForgotForm(Form):
    email = TextAreaField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class SearchForm(Form):
    city = StringField('city', validators=[DataRequired()])
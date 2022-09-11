from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError


class SignUpForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    category = SelectField(label='User type', choices=[
                           'Student', 'Organizer', 'Sponsorer'])
    submit = SubmitField(label="Create account")

class MessageForm(FlaskForm):
    message = StringField(label="Text", validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")

class SearchForm(FlaskForm):
    messageText = StringField(validators=[DataRequired()])
    Search = SubmitField()

class EditProfile(FlaskForm):
    fName = StringField(validators=[DataRequired()])
    lName = StringField(validators=[DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    bio  = StringField(validators=[DataRequired()])
    interest = StringField(validators=[DataRequired()])
    save = SubmitField()

class SponsorshipForm(FlaskForm):
    sponsor = SubmitField()
    sponsored = SubmitField()


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from flask_mde import Mde, MdeField


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


class CreateProjectForm(FlaskForm):
    name = StringField(label="Project Name", validators=[DataRequired()])
    description = MdeField(label="Description", validators=[DataRequired()])
    submit = SubmitField(label="Create project")


class CreateEventForm(FlaskForm):
    name = StringField(label="Event name", validators=[DataRequired()])
    location = StringField(label="Event location", validators=[DataRequired()])
    start_date = DateField(label="Start date of the event",
                           validators=[DataRequired()])
    end_date = DateField(label="End date of the event",
                         validators=[DataRequired()])
    start_time = TimeField(label="Start time of the event",
                           validators=[DataRequired()])
    end_time = TimeField(label="Ennd time of the event",
                         validators=[DataRequired()])
    type = SelectField(label='Type of event', choices=[
        'Exhibition', 'Seminar', 'Science Fair'])
    description = StringField(
        label="Description of the event", validators=[DataRequired()])
    submit = SubmitField(label="Create event")


class EventRegistration(FlaskForm):
    email_01 = StringField(label="Email of first member")
    email_02 = StringField(label="Email of second member")
    email_03 = StringField(label="Email of third member")
    submit = SubmitField(label="Create team")


class redirectCreateProject(FlaskForm):
    submit = SubmitField(label="Submit Project")
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


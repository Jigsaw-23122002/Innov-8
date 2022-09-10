from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError


class SignUpForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    category = SelectField(label='User type', choices=[
                           'Student', 'Organizer', 'Sponsorer'])
    submit = SubmitField(label="Create account")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError

class SignUpForm(FlaskForm):
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Create account")

class LoginForm(FlaskForm):
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Login")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError

class SignUpForm(FlaskForm):

    def validate_email(self,email_to_validate):
        #Check whether the user is already registered or not
        return ''

    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="SignUp")

class LoginForm(FlaskForm):
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Login")
from wtforms import Form, StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class SignUp(Form):

    username = StringField('Username', [
        validators.DataRequired(message=('Please enter a username'))
    ])

    password = PasswordField('NewPassword', [ 
        validators.DataRequired(),
        validators.EqualTo('confirmPassword', message = 'Passwords must match')
    ])

    confirmPassword = PasswordField('NewPassword')

    submit = SubmitField('Register')

class SignUp2(Form):
    fname = StringField('First Name', [
        validators.DataRequired(message=('Enter your first name'))
    ])

    lname = StringField('Last Name', [
        validators.DataRequired(message=('Enter your last name'))
    ])

    email = StringField('Email', [
        validators.DataRequired(message=('Enter your email')),
        validators.Email(message=('Enter a valid email address'))
    ])

    submit = SubmitField('Finish')

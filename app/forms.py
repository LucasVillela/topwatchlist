from flask.ext.wtf import Form
from wtforms import TextField, PasswordField,DateField,validators
#from wtforms.validators import DataRequired


class LoginForm(Form):

    email = TextField('Email', [validators.Required()])
    password = PasswordField('Password',[validators.Required()])

class RegisterForm(Form):
	nickname = TextField('Nickname',[validators.optional()])
	dt_nasc = DateField('Birthday',[validators.optional()])
	email = TextField('Email', [validators.Required()])
	password = PasswordField('Password',[validators.Required()])

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField,validators
#from wtforms.validators import DataRequired
from .models import Client

class LoginForm(Form):

    email = TextField('Email', [validators.Required()])
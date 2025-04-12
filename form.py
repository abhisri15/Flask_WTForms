from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField
from wtforms.validators import InputRequired

class MyForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    freeform = TextAreaField('Free Form')
    selects = SelectField('Select', choices=[('first', 'First'), ('second', 'Second'), ('third', 'Third')])
    radios = RadioField('Radios', default='option1', choices=[('option1', 'Option1'), ('option2', 'Option2 ')])
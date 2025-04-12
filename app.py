from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, \
    BooleanField, Form, FormField, FieldList, ValidationError, DateField
from wtforms.validators import InputRequired, Length, AnyOf, Email
# Validators to make form valid, else if you hit blank form submit also it will accept which makes no sense
from collections import namedtuple

class TelephoneForm(Form):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code')
    number = StringField('Number')

class YearForm(Form):
    year = IntegerField('Year')
    total = IntegerField('Total')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired('Username is required'),
        # Length(min=5, max=25, message='Username must be between 5 and 25 characters')
        AnyOf(['admin', 'user'], message='Username must be either admin or user')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('Password is required'),
        Length(min=5, max=10, message='Password must be between 5 and 10 characters')
    ])
    age = IntegerField('Age', validators=[
        InputRequired('Age is required'),
    ])

    yesno = BooleanField('YesNo', validators=[
    ])

    email = StringField('Email', validators=[
        InputRequired('Email is required'),
        Email(message='Invalid email address')
    ])

class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

class NameForm(LoginForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm), min_entries=3)
    recaptcha = RecaptchaField('Recaptcha')

    def validate_first_name(form, field):
        if not field.data:
            raise ValidationError('First name is required')

class DynamicForm(FlaskForm):
    entrydate = DateField('entrydate')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['WTF_CSRF_ENABLED'] = True  # Disable CSRF for simplicity
    app.config['WTF_CSRF_SECRET_KEY'] = 'Mycsrfsecretkey'
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour
    app.config['RECAPTCHA_PUBLIC_KEY'] = 'Mypublickey'
    app.config['RECAPTCHA_PRIVATE_KEY'] = 'Mysecretkey'

    @app.route('/', methods=['GET','POST'])
    def index():

        user = User(username='admin', age=21, email='valid@gmail.com')

        group = namedtuple('Group', ['year', 'total'])
        g1 = group(year=2020, total=100)
        g2 = group(year=2021, total=200)
        g3 = group(year=2022, total=300)

        data = {'years': [g1, g2, g3]}

        form = NameForm(obj=user, data=data)

        if form.validate_on_submit():
            # form.populate_obj(user)

            # return f'Country Code: {form.home_phone.country_code.data}' \
            #        f' Area Code: {form.home_phone.area_code.data}' \
            #        f' Number: {form.home_phone.number.data} '

            # return f'<h1>Username: {form.username.data} Password: {form.password.data} ' \
            #        f'Age: {form.age.data} YesNo: {form.yesno.data} Email: {form.email.data}</h1>'

            output = '<h1>'
            for field in form.years:
                output += f'Year: {field.year.data}'
                output += f'Total: {field.total.data} <br />'

            output += '</h1>'
            return output

        return render_template('index2.html', form=form)

    @app.route('/dynamic', methods=['GET','POST'])
    def dynamic():

        DynamicForm.name = StringField('Name')

        names = ['middle_name','last_name','nick_name']
        for name in names:
            setattr(DynamicForm, name, StringField(name))

        form = DynamicForm()

        if form.validate_on_submit():
            # Handle form submission
            return f'Date: {form.entrydate.data} Name: {form.name.data}'

        return render_template('dynamic2.html', form=form, names=names)

    return app



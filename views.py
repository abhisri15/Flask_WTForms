from flask import Blueprint, render_template
from .form import MyForm

demo = Blueprint('demo', __name__, template_folder='templates')

@demo.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        results = {
            'email' : form.email.data,
            'password' : form.password.data,
            'freeform' : form.freeform.data,
            'radios' : form.radios.data,
            'selects' : form.selects.data
        }
        return render_template('results.html', **results)
    return render_template('index.html', form=form)
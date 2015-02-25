from flask import render_template
from app import app
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/search')
def search():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",
    		title = 'Home',
    		user = user)


@app.route('/query')
def query():
    form = SearchQueryForm()
    return render_template('login.html',
                           title='Search',
                           form=form)


@app.route('/testform/', methods=['GET', 'POST'])
def testform():
    form = MyForm()
    if form.validate_on_submit():
        return '<html>your name is %s</html>' % form.name.data
    return render_template('testform.html', form=form)


class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])

    def __init__(self):
        super(MyForm, self).__init__(csrf_enabled=False)

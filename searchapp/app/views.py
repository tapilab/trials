from app import app
from flask import render_template
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/search')
def search():
    user = { 'nickname': 'Miguel' }  # fake user
    return '''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Hello, ''' + user['nickname'] + '''</h1>
  </body>
</html>
'''


@app.route('/testform/', methods=['GET', 'POST'])
def testform():
    form = MyForm()
    if form.validate_on_submit():
        return '<html>your name is %s</html>' % form.name.data
    return render_template('form.html', form=form)


class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])

    def __init__(self):
        super(MyForm, self).__init__(csrf_enabled=False)

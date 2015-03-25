
from flask import render_template
from app import forms, app
from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired
import trialsearcher, patient

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#index the docs here
@app.route('/login')
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

# This one is the searching app
@app.route('/testform/', methods=['GET', 'POST'])
def testform():
    form = MyForm()
    if form.validate_on_submit():
        #return '<html>your age is %s</html>\r\n <html>your gender is %s</html>' % (form.age.data,form.gender.data)
        test = Patient(form.age.data,form.gender.data,form.inclusion.data,form.exclusion.data)
        print form.age.data
        searcher = TrialSearcher(RAWDIR, limit=99999)
        results = searcher.search(test._get_query_string())
        return '<html>your results are %s</html>  <html>the patient age is %s</html>' % (results,Patient.age)
    return render_template('testform.html', form=form)


class MyForm(Form):
    #name = StringField('name', validators=[DataRequired()])
    age = IntegerField('Patient Age', validators=[DataRequired()])
    age_unit = SelectField(' ',validators=[DataRequired()],choices=[('year','Year'),('month','Month'),('week','Week'),('day','Day')],coerce=unicode)  ## not done yet
    gender = RadioField(u'Gender', validators=[DataRequired()],choices=[('female','Female'),('male','Male')], coerce=unicode)
    inclusion = TextAreaField('Inclusion Criterial', default=None)
    exclusion = TextAreaField('Exclusion Criterial', default=None)

    def __init__(self):
        super(MyForm, self).__init__(csrf_enabled=False)



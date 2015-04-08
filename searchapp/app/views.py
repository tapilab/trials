RAWDIR = '/Users/JingqianLi/Documents/Courses/Trials/search_results'
INDEXDIR='/Users/JingqianLi/Documents/Courses/Trials/index'

from flask import render_template
from app import forms, app
from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from patient import Patient 
from trialsearcher import TrialSearcher


@app.route('/')
def index():
    return "Print here"

@app.route('/null', methods=['GET', 'POST'])
def init():
    form = HomePage()
    if form.validate_on_submit():
        global searcher
        searcher = TrialSearcher(form.link_to_doc.data, limit=99999)
        return search()
    return render_template("homepage.html", form=form)

# searching page
@app.route('/search/', methods=['GET', 'POST'])
def search():
    form = MyForm()
    if form.validate_on_submit():
        #return '<html>your age is %s</html>\r\n <html>your gender is %s</html>' % (form.age.data,form.gender.data)
        # Try biomarker: estrogen receptor
        searcher = TrialSearcher()
        patient_file = Patient(form.age.data,form.age_unit.data,form.gender.data,form.biomarker.data)
        results = searcher.search(patient_file._get_query_string())
        return results(u'results')
        #return '<html>your results are %s</html>  <html>the patient age is %s</html>' % (results,patient_file.age)
    return render_template('search.html', form=form)

@app.route('/results/<results>/', methods=['POST'])
def results(results):
    return render_template('results.html', results=results)


class HomePage(Form):
    link_to_doc = StringField('Documents location:', validators=[DataRequired()])

    def __init__(self):
        super(HomePage, self).__init__(csrf_enabled=False)

class resultForm(Form):
    def __init__(self):
        super(resultForm,self).__init__(csrf_enabled=False)

class MyForm(Form):
    age = IntegerField('Patient Age', validators=[DataRequired()])
    age_unit = SelectField(' ',validators=[DataRequired()],choices=[('year','Year'),('month','Month'),('week','Week'),('day','Day')],coerce=unicode)  ## not done yet
    gender = RadioField(u'Gender', validators=[DataRequired()],choices=[('female','Female'),('male','Male')], coerce=unicode)
    biomarker = TextAreaField('Biomarker', validators=[DataRequired()])

    def __init__(self):
        super(MyForm, self).__init__(csrf_enabled=False)

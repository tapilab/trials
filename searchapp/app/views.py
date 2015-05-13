RAWDIR = '/Users/JingqianLi/Documents/Courses/Trials/search_results'
INDEXDIR='/Users/JingqianLi/Documents/Courses/Trials/index'

from flask import render_template
from app import app
from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from patient import Patient 
from trialsearcher import TrialSearcher
from . import searcher
from colorama import init, Fore
import re

@app.route('/')
def index():
    return "Print here"

# searching page
@app.route('/search/', methods=['GET', 'POST'])
def search():
    form = MyForm()
    results = None
    resultsPrint = None
    if form.validate_on_submit():
        # Try biomarker: estrogen receptor
        patient_file = Patient(form.age.data,form.age_unit.data,form.gender.data,form.biomarker.data)
        results = searcher.search(patient_file._get_query_string())
        resultsPrint = searcher.print_results(results,form.biomarker.data)
        print resultsPrint
        redString = Highlight(resultsPrint)
        print redString.highlight(form.biomarker.data)
        print form.biomarker.data
        # return '<br>'.join([str(x) for x in results3])  # results(u'results')
        #return '<html>your results are %s</html>  <html>the patient age is %s</html>' % (results,patient_file.age)
    return render_template('search.html', form=form, results = resultsPrint)

class MyForm(Form):
    age = IntegerField('Patient Age', validators=[DataRequired()])
    age_unit = SelectField(' ',validators=[DataRequired()],choices=[('year','Year'),('month','Month'),('week','Week'),('day','Day')],coerce=unicode)  ## not done yet
    gender = RadioField(u'Gender', validators=[DataRequired()],choices=[('female','Female'),('male','Male')], coerce=unicode)
    biomarker = TextAreaField('Biomarker', validators=[DataRequired()])

    def __init__(self):
        super(MyForm, self).__init__(csrf_enabled=False)

class Highlight:
    def __init__(self, string):
        self.s = string

    def highlight(self,biomarker):
        sred = re.sub(biomarker, Fore.RED + r'\1' + Fore.RESET, self.s)
        return sred

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class SearchQureyForm(Form):
    age = IntegerField('Patient Age', validators=[DataRequired()])  ## not done yet
    gender = StringField('Gender', validators=[DataRequired()])
    inclusion = StringField('Inclusion Criterial', default=None)
    exclusion = StringField('Exclusion Criterial', default=None)

    def __init__(self):
        super(SearchQureyForm, self).__init__(csrf_enabled=False)
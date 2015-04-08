from whoosh.query import *

class Patient:
    """ Create an patient object that has fields from the trial entity """
    
    #query = ''
    
    def __init__(self, age, age_unit, gender, biomarker):
        self.myage = self._convert_birthdate(age,age_unit)
        self.mygender = gender
        self.mybiomarker = biomarker
        print self.myage
        
    def _get_query_string(self):
        myquery = And([NumericRange('minimum_age', 0, self.myage),
                       NumericRange('maximum_age', self.myage, 99999),
                       Phrase('inclusion',self.mybiomarker.split()),
                       Not(Phrase('exclusion', self.mybiomarker.split())),
                       Or([Term('gender',self.mygender), Term('gender','both'), Term('gender', 'N/A')])])
        return str(myquery.normalize())
    
    def _convert_birthdate(self,age,age_unit):
        if age_unit == 'day':
            return age
        elif age_unit == 'week':
            return 7*age
        elif age_unit == 'month':
            return 30*age
        else:
            return 365*age
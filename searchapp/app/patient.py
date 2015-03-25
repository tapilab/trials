# This calss is for patient object


class Patient:
    """ Create an patient object that has fields from the trial entity """
    
    def __init__(self, age, gender, inclusion, exclusion):
        self.query = self._csv_to_query(age,gender,inclusion,exclusion)
    
    def _csv_to_query(self, age, gender, inclusion, exclusion):
        myage = self._convert_birthdate(age)
        mygender = self._convert_gender(gender)
        myquery = And([NumericRange('minimum_age', 0, myage),
                       NumericRange('maximum_age', myage, 99999),
                       Phrase('inclusion',inclusion), #Term('exclusion', biomarker),
                       Not(Phrase('exclusion', exclusion)),
                       Or([Term('gender',mygender), Term('gender','both'), Term('gender', 'N/A')])])
        return myquery
        
    def _get_query_string(self):
        return str(self.query.normalize())
    
    def _convert_birthdate(self,age):
        # fix that part to translate a string input to age
        try:
            month, day, year = [int(x) for x in age.split("/")]   # The format example is: 2/1/91
        except:
            print "Birth date is not valid!"
        today = date.today()
        if ((year+2000)>today.year):
            year = year+1900
        else:
            year = year+2000
        birth = date(year,month,day)
        time_to_today = abs(birth-today)
        return time_to_today.days
    
    def _convert_gender(self, gender):
        try: 
            new_gender = gender.lower()
        except: 
            print "Gender is not valid"
        return new_gender



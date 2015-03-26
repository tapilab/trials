
# Clinical Trial Data

"""We download clinical trials from [ClinicalTrials.gov](http://clinicaltrials.gov)
and create a search engine using [Whoosh](https://pythonhosted.org/Whoosh/)."""


# RAWDIR stores the search results from ClinicalTrials.gov, one trial per xml file.
#RAWDIR='/Users/JingqianLi/Documents/Courses/Trials/search_result'

RAWDIR = '/Users/JingqianLi/Documents/Courses/Trials/SEARCH_TEST'
    
# The search index will be stored here.
INDEXDIR='/Users/JingqianLi/Documents/Courses/Trials/index'
#!mkdir -p $INDEXDIR

import glob 
import io
import sys, traceback
import re
import time
import csv

from datetime import date     
from lxml import etree
import xml.etree.ElementTree as ET
from whoosh.fields import KEYWORD, DATETIME, ID, Schema, TEXT, NUMERIC
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import whoosh.qparser as qparser
from whoosh.query import *
    
class TrialSearcher:
    """ Index a list of trial xml documents to support fielded queries. """
        
    def __init__(self, xml_dir, limit=99999):
        """
        Params:
          xml_dir ... path containing a list of xml files, one per trial.
          limit ..... maximum number of xml files to index, for testing. """
        self._create_index(xml_dir, limit)
            
    def _find_text(self, element, xpathq):
        """ Return the text contents of the results of an xpath query on this element.
        Params:
          element ... root XML element to search
          xpathq .... An XPath query to run.
        Returns:
          A string containing the text portion of the matching element. If there
          multiple matches, they are concatenated. """
        matches = [x for x in element.xpath(xpathq)]
        return u' '.join(unicode(m.text.strip()) for m in matches)
        
    def _add_doc(self, xmlfile, writer):
        """ Add a single trial XML file as a document in the index.
        Params:
          xmlfile ... Path to trial XML file.
          writer .... The IndexWriter."""
        tree = etree.parse(io.open(xmlfile, encoding='utf8'))
        for study in tree.xpath("//clinical_study"):
            
            if (self._find_text(study, '//eligibility/maximum_age').lower() != 'n/a'):
                maximum_age = self._convert_age_to_day(self._find_text(study, '//eligibility/maximum_age').lower())
            else :
                maximum_age = 73000                    # set to 200 years old if maximum age is N/A
                
            if (self._find_text(study, '//eligibility/minimum_age').lower() != 'n/a'):
                minimum_age = self._convert_age_to_day(self._find_text(study, '//eligibility/minimum_age').lower())
            else :
                minimum_age = 0
            
            criteria = self._find_text(study, '//eligibility/criteria/textblock')
            m = re.search(r'Exclusion', criteria)
            inclusion = criteria
            exclusion = u' '
            if m:
                listCriteria = re.split(r'Exclusion', criteria)
                inclusion = listCriteria[0]
                exclusion = listCriteria[1]
            
            d = {
                'completion_date': self._find_text(study, '//completion_date'),
                'inclusion': inclusion,
                'exclusion': exclusion,
                'gender': self._find_text(study, '//eligibility/gender'),
                'healthy_volunteers': self._find_text(study, '//eligibility/healthy_volunteers'),
                'locations': self._find_text(study, '//location_countries/country'),
                'maximum_age': maximum_age,
                'minimum_age': minimum_age,
                'nct_id': self._find_text(study, '//id_info/nct_id'),
                'title': self._find_text(study, '//brief_title'),
                'source': self._find_text(study, '//source'),
                'start_date': self._find_text(study, '//start_date'),
                }
            # FIXME: consider Boolean, Numeric field types.
            writer.add_document(**d)
   
    def _convert_age_to_day(self,age_str):
        t = int(re.findall(r'\d+',age_str)[0])
        if (age_str.find('days') != -1):
            age = t
        elif (age_str.find('weeks') != -1 or age_str.find('week') != -1):
            age = t * 7
        elif (age_str.find('months') != -1 or age_str.find('month') != -1):
            age = t * 30
        elif (age_str.find('years') != -1 or age_str.find('year') != -1):
            age = t * 365
        else :
            print 'exception!'
        return age
    
    def _convert_day_to_age(self,day):
        year = day/365
        return year
        
    def _create_index(self, xml_dir, limit):
        """ Create an index containing the contents of the trial xml directory.
        Params:
          xml_dir ... path to list of trial xml files.
          limit ..... Only read this many xml files, for testing."""
        schema = Schema(
                        completion_date=TEXT,
                        inclusion=TEXT(stored=True),
                        exclusion=TEXT(stored=True),
                        gender=TEXT(stored=True),
                        healthy_volunteers=TEXT,
                        locations=TEXT,
                        maximum_age=NUMERIC(stored=True),
                        minimum_age=NUMERIC(stored=True),     
                        nct_id=ID(stored=True),
                        title=TEXT(stored=True),
                        source=TEXT,
                        start_date=TEXT,
                        )
    
        self.index = create_in(INDEXDIR, schema)
        writer = self.index.writer(limitmb=99999)  # CHANGE THE LIMIT
        count = 0
        for xmlfile in glob.glob(xml_dir + '/*.xml'):    # ??
            try:
                self._add_doc(xmlfile, writer)
            except:
                print 'cannot parse file %s' % xmlfile
            count += 1
            if count % 100 == 0:
                print 'indexed %d documents' % count
            if count == limit:
                break
        writer.commit()
    
    def search(self, query_str, limit=100):
        """ Exectue a query on this index.
        Params:
          query_str: A possibly fielded query string. Searches the 'inclusion' field by default.
          limit: Maximum number of results to return.
        Return:
          A rank-ordered list of document ids."""
        parser = QueryParser('inclusion',schema=self.index.schema, group=qparser.OrGroup)
        with self.index.searcher() as searcher:
            query = parser.parse(query_str)
            results = searcher.search(query, limit=limit)
            return [r.docnum for r in results]
        
    def print_results(self, results):
        """ Print to stdout a list of search results.
        Params:
          results: A rank-ordered list of document ids."""
        with self.index.searcher() as searcher:    #returns an iterator of docnums matching this query
            for r in results:
                doc = searcher.stored_fields(r)
                print '\t'.join([doc['nct_id'], doc['title']]), 'Gender: ', doc['gender']
                print 'maximum age is: ', doc['maximum_age'],' days, and minimum_age is: ', doc['minimum_age'], ' days'
                print 'Exclusion: ', doc['exclusion']
                print 'Inclusion: ', doc['inclusion']

                
            
# This calss is for patient object


class Patient:
    """ Create an patient object that has fields from the trial entity """
    
    #query = ''
    
    def __init__(self, csvfile):
        self.query = self._csv_to_query(csvfile)
    
    def _csv_to_query(self,csvfile):
        with open(csvfile) as f:
            f_csv = csv.DictReader(f)
            a_list = []
            i = 0
            for row in f_csv:
                a_list.append(row)
                #print a_list[i], '\n'
                i += 1
        dic = a_list[99]  # Pick up a case of patient randomly
        print dic['DATE_OF_BIRTH']
        biomarker = dic['LONG_NAME']
        myage = self._convert_birthdate(dic['DATE_OF_BIRTH'])
        mygender = self._convert_gender(dic['GENDER'])
        myquery = And([NumericRange('minimum_age', 0, myage),
                       NumericRange('maximum_age', myage, 99999),
                       Phrase('inclusion',biomarker.split()), #Term('exclusion', biomarker),
                       Not(Phrase('exclusion', biomarker.split())),
                       Or([Term('gender',mygender), Term('gender','both'), Term('gender', 'N/A')])])
        return myquery
        
    def _get_query_string(self):
        return str(self.query.normalize())
    
    def _convert_birthdate(self,age):
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


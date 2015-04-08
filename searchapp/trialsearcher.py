
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
from whoosh.index import open_dir
from whoosh.filedb.filestore import FileStorage 
    
class TrialSearcher:
    """ Index a list of trial xml documents to support fielded queries. """
    
        
    def __init__(self):
        """
        Params:
          xml_dir ... path containing a list of xml files, one per trial.
          limit ..... maximum number of xml files to index, for testing. """
        storage = FileStorage('/Users/JingqianLi/Documents/Courses/Trials/index')
        self.index = storage.open_index() # index should be created by index.py
        print storage.open_index()
    
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
                
            
# This calss is for patient object


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


from whoosh.fields import KEYWORD, DATETIME, ID, Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import whoosh.qparser as qparser
from whoosh.query import *
from whoosh.filedb.filestore import FileStorage 
from colorama import init, Fore 
import re
import HTMLParser
from whoosh.highlight import *


class TrialSearcher:
    """ Index a list of trial xml documents to support fielded queries. """
    
        
    def __init__(self):
        """
        Params:
          xml_dir ... path containing a list of xml files, one per trial.
          limit ..... maximum number of xml files to index, for testing. """
        storage = FileStorage('/Users/JingqianLi/Documents/Courses/Trials/index')
        self.index = storage.open_index() # index should be created by index.py
    
    def search(self, query_str, limit=100):
        """ Exectue a query on this index.
        Params:
          query_str: A possibly fielded query string. Searches the 'inclusion' field by default.
          limit: Maximum number of results to return.
        Return:
          A rank-ordered list of document ids."""
        parser = qparser.QueryParser('inclusion',schema=self.index.schema, group=qparser.OrGroup)
        with self.index.searcher() as searcher:
            query = parser.parse(query_str)
            results = searcher.search(query, limit=limit)
            return [r.docnum for r in results]
        
    def print_results(self, results,biomarker):
        """ Print to stdout a list of search results.
        Params:
          results: A rank-ordered list of document ids."""
        string = ''
        html_parser = HTMLParser.HTMLParser()

        with self.index.searcher() as searcher:    #returns an iterator of docnums matching this query
            for r in results:
                doc = searcher.stored_fields(r)
                pattern = r'(' + re.escape(biomarker) + ')'
                string += '<b>' + '\t'.join([doc['nct_id'], doc['title']]) + '</b>'
                string += '<p>' + 'Gender: ' + doc['gender'] + '</p>'
                string += '<p>' + 'maximum age is: ' + str(doc['maximum_age']) + ' days, and minimum_age is: ' + str(doc['minimum_age']) + ' days' +'</p>'
                string += '<b>' + 'Inclusion: ' + '</b>' + '<p>'+ re.sub(pattern, r'<b><font color="red">\1</font></b>', doc['inclusion']) + '</p>'
                string += '<b>' + 'Exclusion: ' '</b>' + '<p>' + doc['exclusion'] + '</p>'
        return string


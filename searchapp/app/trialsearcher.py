from whoosh.fields import KEYWORD, DATETIME, ID, Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import whoosh.qparser as qparser
from whoosh.query import *
from whoosh.filedb.filestore import FileStorage 
from whoosh import highlight
from colorama import init, Fore
import re
    
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
            results.fragmenter = highlight.SentenceFragmenter()
            for hit in results:
                print (hit.highlights("inclusion"))
            return [r.docnum for r in results]
        
    def print_results(self, results):
        """ Print to stdout a list of search results.
        Params:
          results: A rank-ordered list of document ids."""
        string = ''
        with self.index.searcher() as searcher:    #returns an iterator of docnums matching this query
            for r in results:
                doc = searcher.stored_fields(r)
                string += '\t'.join([doc['nct_id'], doc['title']]) + '\n' + 'Gender: ' + doc['gender']
                string += '\n' + 'maximum age is: ' + str(doc['maximum_age']) + ' days, and minimum_age is: ' + str(doc['minimum_age']) + ' days'
                string += '\n' + 'Exclusion: ' + doc['exclusion']
                string += '\n' + 'Inclusion: ' + doc['inclusion'] + '\n'
                string += re.sub(r'Inclusion'), Fore.RED + r'\1' + Fore.RESET, 
        print string
        return string


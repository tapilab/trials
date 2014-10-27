# RAWDIR stores the search results from ClinicalTrials.gov, one trial per xml file.
RAWDIR='/Users/JingqianLi/Documents/Courses/Trials/search_result'
    
# The search index will be stored here.
INDEXDIR='/Users/JingqianLi/Documents/Courses/Trials/index'
!mkdir -p $INDEXDIR


import glob 
import io
import sys, traceback
import re
    
from lxml import etree
from whoosh.fields import KEYWORD, DATETIME, ID, Schema, TEXT, NUMERIC
from whoosh.index import create_in
from whoosh.qparser import QueryParser
    
class TrialSearcher:
    """ Index a list of trial xml documents to support fielded queries. """
        
    def __init__(self, xml_dir, limit=1000):
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
                max_age = self._find_text(study, '//eligibility/maximum_age').lower()
                p = int(re.findall(r'\d+',max_age)[0])
                if (max_age.find('days') != -1):
                    maximum_age = p 
                elif (max_age.find('months') != -1 or max_age.find('month')):
                    maximum_age = p * 30 
                elif (max_age.find('years') != -1 or max_age.find('year')):
                    maximum_age = p * 365
            else :
                maximum_age = 73000                    # set to 200 years old if maximum age is N/A
                
            if (self._find_text(study, '//eligibility/minimum_age').lower() != 'n/a'):
                min_age = self._find_text(study, '//eligibility/minimum_age').lower()
                t = int(re.findall(r'\d+',min_age)[0])
                if (min_age.find('days') != -1):
                    minimum_age = t
                elif (min_age.find('months') != -1 or min_age.find('month') != -1):
                    minimum_age = t * 30
                elif (min_age.find('years') != -1 or min_age.find('year') != -1):
                    minimum_age = t * 365
            else :
                minimum_age = 0
            
            d = {
                'completion_date': self._find_text(study, '//completion_date'),
                'criteria': self._find_text(study, '//eligibility/criteria/textblock'),
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
            
    def _create_index(self, xml_dir, limit):
        """ Create an index containing the contents of the trial xml directory.
        Params:
          xml_dir ... path to list of trial xml files.
          limit ..... Only read this many xml files, for testing."""
        schema = Schema(
                        completion_date=TEXT,
                        criteria=TEXT(stored=True),
                        gender=TEXT,
                        healthy_volunteers=TEXT,
                        locations=TEXT,
                        maximum_age=NUMERIC(stored=True),      #change the ID type to numeric, invert the unit to DAYS
                        minimum_age=NUMERIC(stored=True),     
                        nct_id=ID(stored=True),
                        title=TEXT(stored=True),
                        source=TEXT,
                        start_date=TEXT
                        )
    
        self.index = create_in(INDEXDIR, schema)
        writer = self.index.writer(limitmb=1000)  # CHANGE THE LIMIT
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
          query_str: A possibly fielded query string. Searches the 'criteria' field by default.
          limit: Maximum number of results to return.
        Return:
          A rank-ordered list of document ids."""
        parser = QueryParser('criteria', schema=self.index.schema)
        with self.index.searcher() as searcher:
            query = parser.parse(query_str)
            print 'query=', query
            results = searcher.search(query, limit=limit)
            return [r.docnum for r in results]
        
    def print_results(self, results):
        """ Print to stdout a list of search results.
        Params:
          results: A rank-ordered list of document ids."""
        with self.index.searcher() as searcher:    #returns an iterator of docnums matching this query
            for r in results:
                doc = searcher.stored_fields(r)
                print '\t'.join([doc['nct_id'], doc['title']])
    
searcher = TrialSearcher(RAWDIR, limit=12131)

results = searcher.search(u'gender:both AND criteria:cancer AND criteria:thyroid AND healthy_volunteers:Accepts AND age:34')  # Caution! no spaces after ':'
print 'results='
searcher.print_results(results)

"""query= (gender:both AND criteria:cancer AND criteria:thyroid AND healthy_volunteers:accepts)  
results=
NCT01149161 Extent of Central Lymph Node Dissection in Papillary Thyroid Microcarcinoma
NCT01109420 Clinical and Genetic Studies in Familial Non-medullary Thyroid Cancer
NCT00999557 Bimatoprost Ophthalmic Solution in Increasing Eyebrow and Eyelash Growth in Patients Who Have Undergone Chemotherapy for Breast Cancer and in Healthy Participants


"""

# use 
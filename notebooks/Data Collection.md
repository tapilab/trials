
# Clinical Trial Data

We download clinical trials from [ClinicalTrials.gov](http://clinicaltrials.gov)
and create a search engine using [Whoosh](https://pythonhosted.org/Whoosh/).


    # RAWDIR stores the search results from ClinicalTrials.gov, one trial per xml file.
    RAWDIR='/data/trials/search_result'
    
    # The search index will be stored here.
    INDEXDIR='/data/trials/index'
    !mkdir -p $INDEXDIR


    import glob 
    import io
    import sys, traceback
    
    from lxml import etree
    from whoosh.fields import KEYWORD, DATETIME, ID, Schema, TEXT
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
                d = {
                    'completion_date': self._find_text(study, '//completion_date'),
                    'criteria': self._find_text(study, '//eligibility/criteria/textblock'),
                    'gender': self._find_text(study, '//eligibility/gender'),
                    'healthy_volunteers': self._find_text(study, '//eligibility/healthy_volunteers'),
                    'locations': self._find_text(study, '//location_countries/country'),
                    'maximum_age': self._find_text(study, '//eligibility/maximum_age'),
                    'minimum_age': self._find_text(study, '//eligibility/minimum_age'),
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
                            maximum_age=ID,
                            minimum_age=ID,
                            nct_id=ID(stored=True),
                            title=TEXT(stored=True),
                            source=TEXT,
                            start_date=TEXT
                            )
    
            self.index = create_in(INDEXDIR, schema)
            writer = self.index.writer(limitmb=1000)
            count = 0
            for xmlfile in glob.glob(xml_dir + '/*.xml'):
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
            with self.index.searcher() as searcher:
                for r in results:
                    doc = searcher.stored_fields(r)
                    print '\t'.join([doc['nct_id'], doc['title']])
    
    searcher = TrialSearcher(RAWDIR, limit=4000)

    indexed 100 documents
    indexed 200 documents
    indexed 300 documents
    indexed 400 documents
    indexed 500 documents
    indexed 600 documents
    indexed 700 documents
    indexed 800 documents
    indexed 900 documents
    indexed 1000 documents
    indexed 1100 documents
    indexed 1200 documents
    indexed 1300 documents
    indexed 1400 documents
    indexed 1500 documents
    indexed 1600 documents
    indexed 1700 documents
    indexed 1800 documents
    indexed 1900 documents
    indexed 2000 documents
    indexed 2100 documents
    indexed 2200 documents
    indexed 2300 documents
    indexed 2400 documents
    indexed 2500 documents
    indexed 2600 documents
    indexed 2700 documents
    indexed 2800 documents
    indexed 2900 documents
    indexed 3000 documents
    indexed 3100 documents
    indexed 3200 documents
    indexed 3300 documents
    indexed 3400 documents
    indexed 3500 documents
    indexed 3600 documents
    indexed 3700 documents
    indexed 3800 documents
    indexed 3900 documents
    indexed 4000 documents



    # Example query.
    results = searcher.search(u'gender:both AND criteria:cancer AND criteria:thyroid AND healthy_volunteers:Accepts')  # Caution! no spaces after ':'
    print 'results='
    searcher.print_results(results)

    query= (gender:both AND criteria:cancer AND criteria:thyroid AND healthy_volunteers:accepts)
    results=
    NCT01149161	Extent of Central Lymph Node Dissection in Papillary Thyroid Microcarcinoma
    NCT01109420	Clinical and Genetic Studies in Familial Non-medullary Thyroid Cancer
    NCT00999557	Bimatoprost Ophthalmic Solution in Increasing Eyebrow and Eyelash Growth in Patients Who Have Undergone Chemotherapy for Breast Cancer and in Healthy Participants


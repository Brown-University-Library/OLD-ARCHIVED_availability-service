# -*- coding: utf-8 -*-

import json, logging, unittest
from backend import Search


formatter = logging.Formatter( u'%(asctime)s - %(levelname)s - %(message)s' )
logger = logging.getLogger()
logger.setLevel( logging.INFO )
console_handler = logging.StreamHandler()
console_handler.setFormatter( formatter )
logger.addHandler( console_handler )


class z39Test( unittest.TestCase ):
    """ Tests brown fork of PyZ3950. """

    def setUp(self):
        self.z39 = Search( logger )
        self.book_bib = 'b3386235'
        self.journal_bib = 'b4074295'
        self.online_journal_bib = 'b7091233'

    def tearDown(self):
        self.z39.close()

    def test_z39lib_unicode_param(self):
        """ Tests lib unicode handling. """
        try:
            rsp = self.z39.id( unicode(self.book_bib) )
        except Exception as e:
            expected = u"<class 'PyZ3950.zoom.QuerySyntaxError'>"
            self.assertEqual( expected, unicode(type(e)) )

    def test_z39_book(self):
        """ Tests returned book data. """
        ## service returns list
        rsp = self.z39.id( self.book_bib )
        # print( json.dumps(rsp, indent=2) )
        expected = list
        self.assertEqual( expected, type(rsp) )
        ## list of dicts
        item = rsp[0]
        expected = dict
        self.assertEqual( expected, type(item) )
        expected = ['barcodes', 'id', 'isbn', 'items', 'lccn', 'oclc', 'summary', 'title', 'url']
        self.assertEqual( expected, sorted(item.keys()) )
        ## id reflected back
        expected = self.book_bib
        self.assertEqual( expected, item[u'id'] )
        ## tho utf-strings required as param, returned values are unicode
        self.assertEqual( unicode, type(item[u'id']) )

    def test_z39_journal(self):
        """ Tests returned journal data. """
        rsp = self.z39.id( self.journal_bib )
        item = rsp[0]
        expected = ['barcodes', 'id', 'isbn', 'items', 'lccn', 'oclc', 'summary', 'title', 'url']
        self.assertEqual( expected, sorted(item.keys()) )

    def test_z39_online_journal(self):
        """ Tests returned online-journal data. """
        rsp = self.z39.id( self.online_journal_bib )
        item = rsp[0]
        expected = ['barcodes', 'id', 'isbn', 'items', 'lccn', 'summary', 'title', 'url']
        self.assertEqual( expected, sorted(item.keys()) )



if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()

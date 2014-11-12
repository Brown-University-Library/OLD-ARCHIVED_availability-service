# -*- coding: utf-8 -*-

"""
z3950_wrapper.py unit tests
"""

import json, logging, os, pprint, unittest
from z3950_wrapper import Searcher


def setup_logger():
    """ Returns a logger to write to a file.
        Assumes os handles log-rotate. """
    LOG_DIR = unicode( os.environ.get(u'availability__LOG_DIR') )
    LOG_LEVEL = unicode( os.environ.get(u'availability__LOG_LEVEL') )
    filename = u'%s/availability_service.log' % LOG_DIR
    formatter = logging.Formatter( u'[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s' )
    logger = logging.getLogger( __name__ )
    level_dict = { u'debug': logging.DEBUG, u'info':logging.INFO }
    logger.setLevel( level_dict[LOG_LEVEL] )
    file_handler = logging.FileHandler( filename )
    file_handler.setFormatter( formatter )
    logger.addHandler( file_handler )
    return logger


class SearcherTest( unittest.TestCase ):
    """ Tests z3950_wrapper.Searcher() wrapper around Brown's fork of PyZ3950. """

    def setUp(self):
        self.srchr = Searcher( setup_logger() )
        self.srchr.connect()
        self.book_bib = u'b3386235'
        self.journal_bib = u'b4074295'
        self.online_journal_bib = u'b7091233'
        self.oclc_num = u'ocm41356566'
        self.isbn = u'0688002307'

    def tearDown(self):
        self.srchr.close_connection()

    def test_book_isbn_explicit(self):
        """ Tests returned book data using explicit function calls. """
        qstring = self.srchr.build_qstring( u'isbn', self.isbn )
        qobject = self.srchr.build_qobject( qstring )
        resultset = self.srchr.connection.search( qobject )
        item_list = self.srchr.process_resultset( resultset, marc_flag=True )  # marc_flag typically False
        # pprint.pprint( item_list )
        ## service returns list
        self.assertEqual( list, type(item_list) )
        ## list of dicts
        self.assertEqual( dict, type(item_list[0]) )
        ## data
        expected = [u'bibid', u'callnumber', u'holdings_data', u'isbn', u'item_barcode', u'itemid', u'josiah_bib_url', u'lccn', u'oclc_brown', u'raw_marc', u'title']
        self.assertEqual( expected, sorted(item_list[0].keys()) )
        ## id reflected back
        expected = self.isbn
        self.assertEqual( expected, item_list[0][u'isbn'] )
        ## values unicode
        self.assertEqual( unicode, type(item_list[0][u'isbn']) )

    def test_book_isbn_simple(self):
        """ Tests returned book data using covenience function. """
        item_list = self.srchr.search( key=u'isbn', value=self.isbn, marc_flag=False )
        ## service returns list
        self.assertEqual( list, type(item_list) )
        ## list of dicts
        self.assertEqual( dict, type(item_list[0]) )
        ## data
        expected = [u'bibid', u'callnumber', u'holdings_data', u'isbn', u'item_barcode', u'itemid', u'josiah_bib_url', u'lccn', u'oclc_brown', u'title']
        self.assertEqual( expected, sorted(item_list[0].keys()) )
        ## id reflected back
        expected = self.isbn
        self.assertEqual( expected, item_list[0][u'isbn'] )
        ## values unicode
        self.assertEqual( unicode, type(item_list[0][u'isbn']) )

    def test_journal_bib(self):
        """ Tests returned journal data. """
        item_list = self.srchr.search( key=u'bib', value=self.journal_bib, marc_flag=False )
        expected = [u'bibid', u'callnumber', u'holdings_data', u'isbn', u'item_barcode', u'itemid', u'josiah_bib_url', u'lccn', u'oclc_brown', u'title']
        self.assertEqual( expected, sorted(item_list[0].keys()) )

    def test_online_journal_bib(self):
        """ Tests returned online-journal data. """
        item_list = self.srchr.search( key=u'bib', value=self.online_journal_bib, marc_flag=False )
        expected = [u'bibid', u'callnumber', u'holdings_data', u'isbn', u'item_barcode', u'itemid', u'josiah_bib_url', u'lccn', u'oclc_brown', u'title']
        self.assertEqual( expected, sorted(item_list[0].keys()) )

    def test_book_oclc(self):
        """ Tests returned online-journal data. """
        item_list = self.srchr.search( key=u'oclc', value=self.oclc_num, marc_flag=False )
        expected = [u'bibid', u'callnumber', u'holdings_data', u'isbn', u'item_barcode', u'itemid', u'josiah_bib_url', u'lccn', u'oclc_brown', u'title']
        self.assertEqual( expected, sorted(item_list[0].keys()) )




if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()

# -*- coding: utf-8 -*-

"""
Experimenting w/z3950 library.
Resources:
- z3950 library docs, http://www.panix.com/~asl2/software/PyZ3950/zoom.html
- list of record formats,  http://lists.indexdata.dk/pipermail/zoom/2003-November/000547.html
"""

import logging, os, pprint, sys
from PyZ3950 import zoom  # fork, git+https://github.com/Brown-University-Library/PyZ3950.git
from pymarc import Record  # pymarc==3.0.2


class Experimenter( object ):

    def __init__( self ):
        self.HOST = unicode( os.getenv(u'availability_HOST') )
        self.PORT = unicode( os.getenv(u'availability_PORT') )
        self.DB_NAME = unicode( os.getenv(u'availability_DB_NAME') )
        self.LOG_DIR = unicode( os.environ.get(u'availability__LOG_DIR') )
        self.LOG_LEVEL = unicode( os.environ.get(u'availability__LOG_LEVEL') )
        self.logger = self.setup_logger()
        self.connection = None

    def setup_logger( self ):
        """ Returns a logger to write to a file.
            Assumes os handles log-rotate. """
        filename = u'%s/availability_service.log' % self.LOG_DIR
        formatter = logging.Formatter( u'[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s' )
        logger = logging.getLogger( __name__ )
        level_dict = { u'debug': logging.DEBUG, u'info':logging.INFO }
        logger.setLevel( level_dict[self.LOG_LEVEL] )
        file_handler = logging.FileHandler( filename )
        file_handler.setFormatter( formatter )
        logger.addHandler( file_handler )
        return logger

    def connect( self ):
        conn = zoom.Connection(
            self.HOST,
            int(self.PORT),
            databaseName=self.DB_NAME,
            preferredRecordSyntax=u'OPAC',  # Getting records in "opac" format. (Others were not more helpful.)
            charset=u'utf-8',
            )
        self.connection = conn
        return

    def close_connection( self ):
        self.logger.debug( 'in play.Experimenter.close_connection(); closing connection.')
        self.connection.close()

    def make_error_dict( self ):
        error_dict = {
            u'error-type': sys.exc_info()[0],
            u'error-message': sys.exc_info()[1],
            u'line-number': sys.exc_info()[2].tb_lineno
            }
        return error_dict

    def build_qstring( self, key, value ):
        dct = {
            u'isbn': u'@attr 1=7',
            u'issn': u'@attr 1=8',
        }
        qstring = u'%s %s' % ( dct[key], value )
        self.logger.debug( 'in play.Experimenter.build_qstring(); qstring, `%s`' % qstring )
        return qstring

    def build_qobject( self, qstring ):
        qobject = zoom.Query(
            u'PQF'.encode(u'utf-8'),
            qstring.encode(u'utf-8')
            )
        self.logger.debug( u'in play.Experimenter.build_qobject(); type(qobject), `%s`' % type(qobject) )
        self.logger.debug( u'in play.Experimenter.build_qobject(); pprint.pformat(qobject), `%s`' % pprint.pformat(qobject) )
        return qobject

    def inspect_resultset( self, resultset ):
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(resultset), `%s`' % pprint.pformat(resultset) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(dir(resultset)), `%s`' % pprint.pformat(dir(resultset)) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(resultset.__dict__), `%s`' % pprint.pformat(resultset.__dict__) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(len(resultset)), `%s`' % pprint.pformat(len(resultset)) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(resultset[0]), `%s`' % pprint.pformat(resultset[0]) )
        rec = resultset[0]
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(dir(rec)), `%s`' % pprint.pformat(dir(rec)) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(rec.__dict__), `%s`' % pprint.pformat(rec.__dict__) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(rec.data), `%s`' % pprint.pformat(rec.data) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(rec.data.bibliographicRecord), `%s`' % pprint.pformat(rec.data.bibliographicRecord) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(rec.data.bibliographicRecord.encoding), `%s`' % pprint.pformat(rec.data.bibliographicRecord.encoding) )
        pm_rec = Record( data=rec.data.bibliographicRecord.encoding[1] )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(pm_rec), `%s`' % pprint.pformat(pm_rec) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(dir(pm_rec)), `%s`' % pprint.pformat(dir(pm_rec)) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(pm_rec.__dict__), `%s`' % pprint.pformat(pm_rec.__dict__) )
        exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(pm_rec.as_dict()), `%s`' % pprint.pformat(pm_rec.as_dict()) )

        # exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(rec.data.holdingsData), `%s`' % pprint.pformat(rec.data.holdingsData) )


        result_list = []
        for result in resultset:
            result_entry = {}
            result_entry[u'marc'] = result.data.bibliographicRecord.encoding
            pm_rec = Record( data=result.data.bibliographicRecord.encoding[1] )
            result_entry[u'dict'] = pm_rec.as_dict()
            result_list.append( result_entry )
        return_data = {
            u'resultset_length': len(resultset),
            u'result_list': result_list
            }
        # exp.logger.debug( u'in play.Experimenter.inspect_resultset, pprint.pformat(return_data), `%s`' % pprint.pformat(return_data) )

        return


try:

    exp = Experimenter()
    exp.connect()
    qstring = exp.build_qstring( u'isbn', u'0688002307' )
    qobject = exp.build_qobject( qstring )
    resultset = exp.connection.search( qobject )
    exp.inspect_resultset( resultset )
    1/0

except Exception as e:

    if exp.connection:
        exp.logger.debug( u'in play.py except, error; will close connection' )
        exp.close_connection()
    error_dict = exp.make_error_dict()
    pprint.pprint( error_dict )
    exp.logger.debug( u'in play.py except, error-info, `%s`' % pprint.pformat(error_dict) )

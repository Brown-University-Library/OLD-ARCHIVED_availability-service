# -*- coding: utf-8 -*-

"""
Helper for availability_service.availability_app
"""

import datetime, os
from availability_service.utils import backend
from werkzeug.contrib.cache import FileSystemCache


class HandlerHelper( object ):
    """ Helpers for main api route. """

    def __init__( self, log ):
        self.legit_services = [ u'bib', u'isbn', u'issn', u'oclc' ]  # will enhance; possible TODO: load from yaml config file
        self.log = log
        self.cache_dir = os.getenv( u'availability_CACHE_DIR' )
        self.cache_minutes = int( os.getenv(u'availability_CACHE_MINUTES') ) * 60  # timeout param requires seconds

    def build_query_dict( self, url, key, value ):
        """ Query reflector.
            Called by availability_service.availability_app.handler(). """
        start_time = datetime.datetime.now()
        query_dict = {
            u'url': url,
            u'query_timestamp': unicode(start_time),
            u'service_id': key,
            u'service_value': value
            }
        return query_dict

    def validate( self, key, value ):
        """ Stub for validation. IP checking another possibility.
            Called by availability_service.availability_app.handler(). """
        message = u'init'
        if key not in self.legit_services:
            message = u'service_id bad'
        if message == u'init':
            message = u'good'
        self.log.debug( u'in validate(); message, %s' % message )
        return message

    def build_response_dict( self, key, value ):
        """ Handler for cached z39.50 call and response.
            Called by availability_service.availability_app.handler(). """
        assert type(value) == unicode
        cache = FileSystemCache( self.cache_dir, threshold=500, default_timeout=self.cache_minutes, mode=0664 )  # http://werkzeug.pocoo.org/docs/0.9/contrib/cache/
        cache_key = u'%s_%s' % ( key, value )
        response_dict = cache.get( cache_key )
        if response_dict is None:
            response_dict = self.query_josiah( key, value.encode(u'utf-8') )
            cache.set( cache_key, response_dict )
        return response_dict

    def query_josiah( self, key, utf8_value ):
        """ Perform actual query.
            Called by self.build_response_dict(). """
        z39 = backend.Search( self.log )
        if key == u'bib':
            rsp_list = z39.id( utf8_value )
        elif key == u'isbn':
            rsp_list = z39.isbn( utf8_value )
        elif key == u'issn':
            rsp_list = z39.issn( utf8_value )
        elif key == u'oclc':
            rsp_list = z39.oclc( utf8_value )
        z39.close()
        return { u'backend_response': unicode(repr(rsp_list)), u'response_timestamp': unicode(datetime.datetime.now()) }

    # end class HandlerHelper

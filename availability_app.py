# -*- coding: utf-8 -*-

import datetime, json, os, pprint
import flask
from availability_service.utils import backend, log_helper
from werkzeug.contrib.cache import FileSystemCache


## setup
app = flask.Flask(__name__)
log = log_helper.setup_logger()
log.debug( u'log initialized at %s' % unicode(datetime.datetime.now()) )


@app.route( u'/v2/hello_world/', methods=['GET'] )  # /availability_service/v2/hello_world/
def hello_world():
    log.debug( u'- in availability_app.hello_world(); starting' )
    return_dict = { u'response': u'hi there!' }
    return flask.jsonify( return_dict )

@app.route( u'/v2/<key>/<value>/', methods=['GET'] )  # eg, /availability_service/v2/bib/b1234/
def handler( key, value ):
    log.debug( u'in availability_app.handler(); starting' )
    helper = HandlerHelper()
    query = helper.build_query_dict( flask.request.url, key, value )
    validation = helper.validate( key, value )
    if not validation == u'good':
        return_dict = { u'query': query, u'response': {u'error': validation} }
        return flask.jsonify( return_dict )
    response = helper.build_response_dict( key, value )
    return flask.jsonify( {u'query': query, u'response': response} )


class HandlerHelper( object ):
    """ Helpers for main api route.
        TODO: move to utils.
    """

    def __init__( self ):
        self.legit_services = [ u'bib', u'isbn', u'oclc' ]  # will enhance; possible TODO: load from yaml config file
        self.cache_dir = os.getenv( u'availability_CACHE_DIR' )
        self.cache_minutes = int( os.getenv(u'availability_CACHE_MINUTES') ) * 60  # timeout param requires seconds

    def build_query_dict( self, url, key, value ):
        """ Query reflector. """
        start_time = datetime.datetime.now()
        query_dict = {
            u'url': url,
            u'query_timestamp': unicode(start_time),
            u'service_id': key,
            u'service_value': value
            }
        return query_dict

    def validate( self, key, value ):
        """ Stub for validation. IP checking another possibility. """
        message = u'init'
        if key not in self.legit_services:
            message = u'service_id bad'
        if message == u'init':
            message = u'good'
        log.debug( u'in validate(); message, %s' % message )
        return message

    def build_response_dict( self, key, value ):
        """ Stub for cached z39.50 call and response. """
        assert type(value) == unicode
        cache = FileSystemCache( self.cache_dir, threshold=500, default_timeout=self.cache_minutes, mode=0664 )  # http://werkzeug.pocoo.org/docs/0.9/contrib/cache/
        cache_key = u'%s_%s' % ( key, value )
        if key == u'bib':
            response_dict = cache.get( cache_key )
            if response_dict is None:
                z39 = backend.Search( log )
                rsp_list = z39.id( value.encode(u'utf-8') )
                z39.close()
                output = unicode(repr(rsp_list))
                response_dict = { u'backend_response': output, u'response_timestamp': unicode(datetime.datetime.now()) }
                cache.set( cache_key, response_dict )
        else:
            response_dict = { u'backend_response': u'coming' }
        return response_dict

    # end class HandlerHelper




if __name__ == u'__main__':
    if os.getenv( u'DEVBOX' ) == u'true':
        app.run( host=u'0.0.0.0', debug=True )
    else:
        app.run()

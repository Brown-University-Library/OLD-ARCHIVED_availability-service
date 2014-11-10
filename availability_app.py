# -*- coding: utf-8 -*-

import datetime, json, os, pprint
import flask
from availability_service.utils import backend, log_helper


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

    def build_query_dict( self, url, key, value ):
        """ Query reflector. """
        start_time = datetime.datetime.now()
        query_dict = {
            u'url': url,
            u'start_time': unicode(start_time),
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
        """ Stub for z39.50 call and response. """
        assert type(value) == unicode
        if key == u'bib':
            z39 = backend.Search( log )
            rsp = z39.id( value.encode(u'utf-8') )
            log.debug( u'in availability_app.HandlerHelper.build_response_dict(); rsp, `%s`' % unicode(repr(rsp)) )
            z39.close()
            output = unicode(repr(rsp))
            log.debug( u'in availability_app.HandlerHelper.build_response_dict(); rsp NOW, `%s`' % output )
            response = { u'backend response': output }
        else:
            response = { u'backend response': u'coming' }
        return response

    # end class HandlerHelper




if __name__ == u'__main__':
    if os.getenv( u'DEVBOX' ) == u'true':
        app.run( host=u'0.0.0.0', debug=True )
    else:
        app.run()

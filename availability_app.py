# -*- coding: utf-8 -*-

"""
Routing module.
"""

import datetime, os, pprint
import flask
from availability_service.utils import app_helper, log_helper


## setup

app = flask.Flask(__name__)
log = log_helper.setup_logger()
log.debug( u'log initialized at %s' % unicode(datetime.datetime.now()) )


## routes

@app.route( u'/v2/hello_world/', methods=['GET'] )  # /availability_service/v2/hello_world/
def hello_world():
    log.debug( u'- in availability_app.hello_world(); starting' )
    return_dict = { u'response': u'hi there!' }
    return flask.jsonify( return_dict )

@app.route( u'/v2/<key>/<value>/', methods=['GET'] )  # eg, /availability_service/v2/bib/b1234/
def handler( key, value ):
    log.debug( u'in availability_app.handler(); starting' )
    helper = app_helper.HandlerHelper( log )
    query = helper.build_query_dict( flask.request.url, key, value )
    validation = helper.validate( key, value )
    if not validation == u'good':
        return_dict = { u'query': query, u'response': {u'error': validation} }
        return flask.jsonify( return_dict )
    response = helper.build_response_dict( key, value )
    return flask.jsonify( {u'query': query, u'response': response} )




if __name__ == u'__main__':
    if os.getenv( u'DEVBOX' ) == u'true':
        app.run( host=u'0.0.0.0', debug=True )
    else:
        app.run()

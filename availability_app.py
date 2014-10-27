# -*- coding: utf-8 -*-

import datetime, json, os, pprint
import flask
from availability_service.utils import log_helper


## setup
app = flask.Flask(__name__)
log = log_helper.setup_logger()
log.debug( u'log initialized at %s' % unicode(datetime.datetime.now()) )


@app.route( u'/v2/hello_world/', methods=['GET'] )  # /availability_service/v2/hello_world/
def hello_world():
    log.debug( u'- in availability_app.hello_world(); starting' )
    return_dict = { u'response': u'hi there!' }
    return flask.jsonify( return_dict )




if __name__ == u'__main__':
    if os.getenv( u'DEVBOX' ) == u'true':
        app.run( host=u'0.0.0.0', debug=True )
    else:
        app.run()

# -*- coding: utf-8 -*-

"""
Handles log setup.
Assumes system's logrotate.
"""

import datetime, logging, os


def setup_logger():
    """ Returns a logger to write to a file.
        Called by usep_gh_handler.py and processor.py functions. """
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

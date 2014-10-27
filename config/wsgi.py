# -*- coding: utf-8 -*-

""" Prepares application environment.
    Variables assume project setup like:
    some_enclosing_directory/
        availability_service/
            config/
            availability_app.py
        env_availability/
     """

import os, pprint, sys


## become self-aware, padawan
current_directory = os.path.dirname( os.path.abspath(__file__) )

## vars
ACTIVATE_FILE = os.path.abspath( u'%s/../../env_availability/bin/activate_this.py' % current_directory )
PROJECT_DIR = os.path.abspath( u'%s/../../availability_service' % current_directory )
PROJECT_ENCLOSING_DIR = os.path.abspath( u'%s/../..' % current_directory )
SITE_PACKAGES_DIR = os.path.abspath( u'%s/../../env_availability/lib/python2.6/site-packages' % current_directory )

## virtualenv
execfile( ACTIVATE_FILE, dict(__file__=ACTIVATE_FILE) )  # file loads environmental variables

## sys.path additions
for entry in [PROJECT_DIR, PROJECT_ENCLOSING_DIR, SITE_PACKAGES_DIR]:
 if entry not in sys.path:
   sys.path.append( entry )

from availability_service.availability_app import app as application

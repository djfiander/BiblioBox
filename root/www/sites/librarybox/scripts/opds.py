#!/usr/bin/env python

#
# OPDS handling application
#

from sys import stderr

import bottle
from bottle import route
from catutils import catlookup, catrender

opds_acq = "application/atom+xml;profile=opds-catalog;kind=acquisition"
opds_nav = "application/atom+xml;profile=opds-catalog;kind=navigation"

@route('/')
def index():
    stderr.write("index!\n")
    bottle.response.set_header('Content-Type', opds_nav)
    template = catlookup.get_template("root.xml")
    return catrender(template)

@route('/title')
def title():
    stderr.write("title!\n")
    bottle.response.set_header('Content-Type', opds_acq)
    template = catlookup.get_template("title.xml")
    return catrender(template)

@route('/author')
@route('/author/<au>')
def author(au=None):
    stderr.write("author!\n")
    if 'au' in bottle.request.params:
        au = bottle.request.params['au']

    if au:
        bottle.response.set_header('Content-Type', opds_acq)
        template = catlookup.get_template("author.xml")
    else:
        bottle.response.set_header('Content-Type', opds_nav)
        template = catlookup.get_template("authorbrowse.xml")
        
    return(catrender(template, author_id=au))


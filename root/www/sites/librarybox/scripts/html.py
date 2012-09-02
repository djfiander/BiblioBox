#!/usr/bin/env python

#
# HTML handling application
#

from sys import stderr

import bottle
from bottle import route
from catutils import catlookup, catrender

@route('/')
def index():
    stderr.write("html index!\n")
    template = catlookup.get_template("root.html")
    return catrender(template)

@route('/title')
def title():
    stderr.write("html title!\n")
    template = catlookup.get_template("title.html")
    return catrender(template)

@route('/author')
@route('/author/<au>')
def author(au=None):
    stderr.write("html author!\n")
    if 'au' in bottle.request.params:
        au = bottle.request.params['au']

    if au:
        template = catlookup.get_template("author.html")
    else:
        template = catlookup.get_template("authorbrowse.html")
        
    return(catrender(template, author_id=au))


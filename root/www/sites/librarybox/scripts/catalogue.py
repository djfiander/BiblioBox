#!/usr/bin/env python

from sys import stderr

import bottle
from bottle import route

import sqlite3

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

opds_acq = "application/atom+xml;profile=opds-catalog;kind=acquisition"
opds_nav = "application/atom+xml;profile=opds-catalog;kind=navigation"

catlookup = TemplateLookup(directories=['./templates',
                                        '/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules',
                           disable_unicode=True)

def _render(tmpl, **args):
    try:
        conn = sqlite3.connect("/www/sites/librarybox/data/librarybox.db")
    except sqlite3.OperationalError:
        conn = sqlite3.connect("./data/librarybox.db")

    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    try:
        return tmpl.render(conn=conn, **args)
    finally:
        conn.close()

@route('/admin/test')
def wtf():
    bottle.response.set_header('content-type', 'text/plain')
    return "\n".join(' '.join([k, str(v)]) for (k, v) in bottle.request.environ.items())

@route('/cat')
def index():
    stderr.write("index!\n")
    bottle.response.set_header('Content-Type', opds_nav)
    template = catlookup.get_template("root.xml")
    return _render(template)

@route('/cat/title')
def title():
    stderr.write("title!\n")
    bottle.response.set_header('Content-Type', opds_acq)
    template = catlookup.get_template("title.xml")
    return _render(template)

@route('/cat/author')
@route('/cat/author/<au>')
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
        
    return(_render(template, author_id=au))

bottle.debug(True)

import socket

if socket.gethostname().lower() == 'librarybox':
    bottle.run(server='flup', host='0.0.0.0', port=8080, debug=True)
else:
    bottle.run()

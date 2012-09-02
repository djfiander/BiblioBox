#!/usr/bin/env python

#
# OPDS handling application
#

from sys import stderr
import urllib

import bottle
from bottle import route
from bottle_sqlite import SQLitePlugin

from catutils import catdb, catrender
import queries

opds_acq = 'application/atom+xml;profile=opds-catalog;kind=acquisition'
opds_nav = 'application/atom+xml;profile=opds-catalog;kind=navigation'

import socket

if socket.gethostname().lower() == 'librarybox':
    stderr.write('Opening site database\n')
    dbfile = '/www/sites/librarybox/data/librarybox.db'
else:
    stderr.write('Opening local database\n')
    dbfile = './data/librarybox.db'

# This magically creates a db connection for those routes that
# have a parameter named 'db'
bottle.install(SQLitePlugin(dbfile))

@route('/')
def index():
    stderr.write('index!\n')
    bottle.response.set_header('Content-Type', opds_nav)
    return catrender('root.xml')

@route('/title')
def title(db):
    stderr.write('title!\n')
    bottle.response.set_header('Content-Type', opds_acq)
    return catrender('title.xml', cursor = queries.titlelist(db))

@route('/title/<id>/<fmt>')
def fetch_title(db, id, fmt):
    qparm = (id, fmt)
    cur = db.execute('''SELECT b.filename as fname
                        FROM books b WHERE b.work_id = ?
                                     AND b.format_id = ?''', qparm)
    fname = cur.fetchone()
    if fname is None:
        bottle.abort(404, 'No such book')
    else:
        # fname is actually a sqlite Row object
        bottle.redirect(urllib.quote(fname['fname']))

    # Both abort() and redirect() raise HTTP exceptions, so this
    # will never return normally

@route('/author')
def authorlist(db):
    stderr.write('browse author!\n')
    bottle.response.set_header('Content-Type', opds_nav)
    cur = queries.author_list(db)
    return(catrender('authorbrowse.xml', cursor=cur))

@route('/author/<au>')
def author(db, au=None):
    stderr.write('author!\n')
    bottle.response.set_header('Content-Type', opds_acq)
    author_info = queries.author_info(db, au)
    if author_info is None:
        bottle.abort(404, 'Unknown author id')
    cur = queries.author_works(db, au)
    return(catrender('author.xml', cursor=cur, author_id=au,
                         author_info=author_info))

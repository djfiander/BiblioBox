#!/usr/bin/env python

#
# OPDS handling application
#

from sys import stderr
import urllib

import bottle
from bottle import route
from catutils import catdb, catrender

opds_acq = "application/atom+xml;profile=opds-catalog;kind=acquisition"
opds_nav = "application/atom+xml;profile=opds-catalog;kind=navigation"

@route('/')
def index():
    stderr.write("index!\n")
    bottle.response.set_header('Content-Type', opds_nav)
    return catrender("root.xml")

@route('/title')
def title():
    stderr.write("title!\n")
    bottle.response.set_header('Content-Type', opds_acq)
    return catrender("title.xml")

@route('/title/<id>/<fmt>')
def fetch_title(id, fmt):
    qparm = (id, fmt)
    conn = catdb()
    try:
        cur = conn.execute("""SELECT b.filename as fname
                              FROM books b WHERE b.work_id = ?
                                           AND b.format_id = ?""", qparm)
        fname = cur.fetchone()
        if fname is None:
            bottle.abort(404, 'No such book')
        else:
            # fname is actually a sqlite Row object
            bottle.redirect(urllib.quote(fname['fname']))
    finally:
        conn.close()
    # Both abort() and redirect() raise HTTP exceptions, so this
    # will never return normally

@route('/author')
@route('/author/<au>')
def author(au=None):
    stderr.write("author!\n")
    if 'au' in bottle.request.params:
        au = bottle.request.params['au']

    if au:
        bottle.response.set_header('Content-Type', opds_acq)
        template = "author.xml"
    else:
        bottle.response.set_header('Content-Type', opds_nav)
        template = "authorbrowse.xml"
        
    return(catrender(template, author_id=au))


#!/usr/bin/env python

#
# Miscellaneous utility functions for the catalogue
#

import sqlite3

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

catlookup = TemplateLookup(directories=['./templates',
                                        '/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules',
                           disable_unicode=True)

def catdb():
    try:
        conn = sqlite3.connect("/www/sites/librarybox/data/librarybox.db")
    except sqlite3.OperationalError:
        conn = sqlite3.connect("./data/librarybox.db")

    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    return conn

def catrender(tmpl, **args):
    conn = db_connect()
    try:
        if isinstance(tmp, basestring):
            tmpl = catlookup(tmpl)

        return tmpl.render(conn=conn, **args)
    finally:
        conn.close()


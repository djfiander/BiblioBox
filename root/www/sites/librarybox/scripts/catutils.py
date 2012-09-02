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

def catrender(tmpl, **args):
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

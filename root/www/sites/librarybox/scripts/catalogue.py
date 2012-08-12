#!/usr/bin/env python

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

import sqlite3
import urllib

from flup.server.fcgi import WSGIServer

catlookup = TemplateLookup(directories=['/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules',
                           disable_unicode=True)

def parse_query_string(qs):
    (templ, fields) = qs.split('&', 1)
    params = {}
    for (key, val) in [field.split('=') for field in fields.split('&')]:
        params[key] = urllib.unquote_plus(val)
    return (templ, params)

def app(environ, start_response):
    if ('QUERY_STRING' not in environ) or (environ['QUERY_STRING'] == ''):
        environ['QUERY_STRING'] = 'root.xml'

    qs = environ['QUERY_STRING']

    if '&' in qs:
        (tname, params) = parse_query_string(qs)
    else:
        tname = qs
        params = {}

    try:
        template = catlookup.get_template(tname)
    except exceptions.TemplateLookupException:
        print exceptions.text_error_template().render()
        template = catlookup.get_template('404.html')
        rcode = '404 Page not found'
        ctype = 'text/html'

    try:
        conn = sqlite3.connect("/www/sites/librarybox/data/librarybox.db")
        conn.row_factory = sqlite3.Row
        conn.text_factory = str
        return [template.render(start_response=start_response,
                                conn=conn, environ=environ, params=params)]
    finally:
        conn.close()

if __name__ == '__main__':
    WSGIServer(app, bindAddress=("127.0.0.1", 2005)).run()

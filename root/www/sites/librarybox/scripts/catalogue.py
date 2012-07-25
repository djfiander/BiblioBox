#!/usr/bin/env python

from mako.template import Template
from mako.lookup import TemplateLookup

from flup.server.fcgi import WSGIServer

catlookup = TemplateLookup(directories=['/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules',
                           disable_unicode=True)

kindmap = {
    "root.xml" : "navigation",
    "title.xml": "acquisition",
    "author.xml": "navigation"
}

def app(environ, start_response):
    if 'QUERY_STRING' in environ:
        qs = environ['QUERY_STRING']

        templ = catlookup.get_template(qs)
        ctype = 'application/atom+xml;profile=opds-catalog;kind={}'.format(kindmap[qs])

        start_response('200 OK', [('Content-Type', ctype)])
        yield templ.render(environ=environ)
    else:
        start_response('200 OK', [('Content-Type', 'text/html')])

if __name__ == '__main__':
    WSGIServer(app, bindAddress=("127.0.0.1", 2005)).run()

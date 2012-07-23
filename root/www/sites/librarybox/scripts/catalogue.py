#!/usr/bin/env python

from mako.template import Template
from mako.lookup import TemplateLookup

from flup.server.fcgi import WSGIServer

catlookup = TemplateLookup(directories=['/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules')

def serve_template(templatename, **kwargs):
    mytemplate = catlookup.get_template(templatename)
    return mytemplate.render(**kwargs)

def app(environ, start_response):
    if ('QUERY_STRING' in environ) and (environ['QUERY_STRING'] == 'root.xml'):
        start_response('200 OK', [('Content-Type', 'application/atom+xml;profile=opds-catalog;kind=navigation')])
    else:
        start_response('200 OK', [('Content-Type', 'text/html')])
    yield str(serve_template("catalogue.tmpl", environ=environ))

if __name__ == '__main__':
    WSGIServer(app, bindAddress=("127.0.0.1", 2005)).run()

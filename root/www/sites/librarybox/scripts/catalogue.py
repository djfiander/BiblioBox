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
    if ('QUERY_STRING' not in environ) or (environ['QUERY_STRING'] == ''):
        environ['QUERY_STRING'] = 'root.xml'

    qs = environ['QUERY_STRING']

    try:
        templ = catlookup.get_template(qs)
        rcode = '200 OK'
        ctype = 'application/atom+xml;profile=opds-catalog;kind={}'.format(kindmap[qs])
    except:
        templ = catlookup.get_template('404.html')
        rcode = '404 Page not found'
        ctype = 'text/html'

    start_response(rcode, [('Content-Type', ctype)])
    yield templ.render(environ=environ)

if __name__ == '__main__':
    WSGIServer(app, bindAddress=("127.0.0.1", 2005)).run()

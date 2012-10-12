#!/usr/bin/env python

from sys import stderr

import bottle
from bottle import route

#
# Administrative interface handling, lives under '/admin'
#
bottle.default_app.push()

@route('/test')
def wtf():
    bottle.response.set_header('content-type', 'text/plain')
    return "\n".join(' '.join([k, str(v)]) for (k, v) in bottle.request.environ.items())

admin_app = bottle.default_app.pop()

#
# OPDS interface, lives under '/opds'
#
bottle.default_app.push()
import opds
opds_app = bottle.default_app.pop()

#
# HTML interface, lives under '/cat'
#
bottle.default_app.push()
import html
html_app = bottle.default_app.pop()

#
# Mount the apps at the right spots in the URL hierarchy and get
# the thing running
#
root = bottle.Bottle()
root.mount(admin_app, '/admin')
root.mount(opds_app, '/opds')
root.mount(html_app, '/cat')

bottle.debug(True)

import socket

if socket.gethostname().lower() == 'librarybox':
    bottle.run(root, server='flup', host='0.0.0.0', port=8080, debug=True)
else:
    bottle.run(root, host='0.0.0.0')

#!/usr/bin/env python

import cherrypy

import sqlite3

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

catlookup = TemplateLookup(directories=['/www/sites/librarybox/templates'],
                           module_directory='/tmp/librarybox_modules',
                           disable_unicode=True)

class Catalogue:
    def index(self):
        template = catlookup.get_template("chroot.xml")
        return self._render(template)
    index.exposed = True

    def test(self):
        pass

    def title(self):
        template = catlookup.get_template("chtitle.xml")
        return self._render(template)
    title.exposed = True

    def author(self, au=None):
        if au:
            template = catlookup.get_template("chauthor.xml")
        else:
            template = catlookup.get_template("chauthorbrowse.xml")
            
        return(self._render(template, author_id=au))
    author.exposed = True

    def _render(self, tmpl, **args):
        conn = sqlite3.connect("/www/sites/librarybox/data/librarybox.db")
        try:
            conn.row_factory = sqlite3.Row
            conn.text_factory = str
            return tmpl.render(conn=conn, **args)
        finally:
            conn.close()

class Root:
    pass

# root = Root()
# root.cat = Catalogue()

cherrypy.config.update({'engine.autoreload_on': False,
                        'log.screen': True})

cherrypy.tree.mount(Catalogue(), '/cat', {'/':
                                   {
                                       'tools.trailing_slash.on': False
                                   }
                               })

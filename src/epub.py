#! /usr/bin/env python

import zipfile
import xml.etree.ElementTree as ET


DCprefix = '{http://purl.org/dc/elements/1.1/}'
OPFprefix = '{http://www.idpf.org/2007/opf}'

namespace_map = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'opf':'http://www.idpf.org/2007/opf'
}


class BadEpubFile(Exception):
    pass

def is_epubfile(fname):
    """Returns True if FNAME is a valid EPUB file, False otherwise"""
    if not zipfile.is_zipfile(fname):
        return False

    try:
        zf = zipfile.ZipFile(fname)
        info = zf.getinfo("mimetype")

        fd = zf.open(info, 'r')
        if fd.readline().rstrip() == "application/epub+zip":
            return True
        else:
            return False
    except KeyError:
        # There's no "mimetype" file in the zipfile
        return False
    finally:
        zf.close()

def find_opf(efile):
    """Returns EpubInfo object corresponding to the OPF file in EFILE"""
    for epinfo in efile.infolist():
        if epinfo.filename[-4:] == '.opf':
            return epinfo
    raise BadEpubFile('No OPF File')

class EpubFile(zipfile.ZipFile):
    def __init__(self, file):
        zipfile.ZipFile.__init__(self, file, 'r')
        self.opf = find_opf(self)
        self.metadata = None

    def init_metadata(self):
        root = ET.parse(self.open(self.opf)).getroot()
        meta = root.find(OPFprefix + 'metadata')
        self.metadata = {}
        self.metadata['title'] = meta.find(DCprefix + 'title').text
        for creator in meta.findall(DCprefix + 'creator'):
            if (creator.attrib[OPFprefix + 'role']) == 'aut':
                self.metadata['author'] = creator.text
                break
        id_name = root.attrib['unique-identifier']
        for ident in meta.findall(DCprefix + 'identifier'):
            if ident.attrib['id'] == id_name:
                self.metadata['id'] = ident.text
                break

    def title(self):
        if self.metadata is None:
            self.init_metadata()
        return self.metadata['title']

    def author(self):
        if self.metadata is None:
            self.init_metadata()
        return self.metadata['author']

    def id(self):
        if self.metadata is None:
            self.init_metadata()
        return self.metadata['id']

# register_namespace() is new in Python 2.7
if 'register_namespace' in ET.__dict__:
    for (prefix, uri) in namespace_map:
        ET.register_namespace(prefix, uri)

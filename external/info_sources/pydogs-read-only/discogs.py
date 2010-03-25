# -*- coding: utf-8 -*-

import cStringIO
import datetime
import gzip
import os
import re
import sys
import urllib
import urllib2
# FIXME: Replace lxml with regexp
import lxml.etree


def tree2object(el, Class, **kwargs):
    """
       Converts an xml tree object to python class instance.
       Keyword arguments are passed to class constructor.
       Example :
       xml = '''
       <tag attr1=value1 attr2=value2>
            <subtag1>Text1</subtag1>
            <subtag2>Text2</subtag2>
       </tag>
       '''
       o = tree2object(xml, SomeClass)
       o.subtag1 == Text1
       o.subtag2 == Text2
       o.attr1 == value1
       o.attr2 == value2
    """
    attrs = dict([ (sube.tag, sube.text) for sube in el.getchildren() ])
    attrs.update(el.attrib)

    return Class(attrs, **kwargs)

def tree2list(lst):
    """
        Converts an xml tree object to a list
        Example :
        xml = '''
        <tag>
            <subtag>Text1</subtag>
            <subtag>Text2</subtag>
        </tag>
        '''
        l = tree2list(xml)
        l == [ 'Text1', 'Text2' ]
    """

    return [ subel.text.strip('\n ')
                for subel in lst
                    if subel.text ]

class _LoadableObject(object):
    """
        Loadable object class. Object attributes are set
        from a dictionary passed to class constructor.
    """
    def __init__(self, data={}, type=None):
        self.__type__ = type
        self.load(data)

    def load(self, data):
        for k in getattr(self, '__attrs__', data.iterkeys()):
            setattr(self, k, data.get(k, None))

        self._data = data

class Release(_LoadableObject):
    """
        Release pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible:
            * Release: 'id', 'images', 'artists', 'title', 'labels',
                       'extraartists', 'formats', 'genres', 'styles', 'country',
                       'released', 'notes', 'tracklist'
            * Artist: 'id', 'status', 'type', 'title', 'format', 'label', 'catno'
            * Label: 'id', 'catno', 'status', 'artist', 'title', 'format'
    """

class Track(_LoadableObject):
    """
        Track pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible: 'position', 'title', 'duration'
    """

class Image(_LoadableObject):
    """
        Image pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible: 'height', 'width', 'type', 'uri', 'uri150'
    """

class Label(_LoadableObject):
    """
        Label pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible:
            * Full: 'images', 'name', 'contactinfo', 'profile', 'parentLabel', 'sublables', 'releases'
            * Min: 'catno', 'name'
    """

class Artist(_LoadableObject):
    """
        Artist pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible:
            * Artist: 'images', 'name', 'realname', 'urls', 'namevariations',
                      'aliases', 'releases'
            * Release: 'name', 'role'
    """

    def __init__(self, data, type='Full'):
        if type == 'Release':
            self.__attrs__ = (
                'name', 'role'
                )

        super(Artist, self).__init__(data)

class Label(_LoadableObject):
    """
        Artist pseudoclass. Loaded attibutes can be specified through
        __attrs__ attribute.

        Avalible:
            * Label: 'images', 'name', 'contactinfo', 'profile', 'urls',
                     'sublabels', 'releases'
    """

class ApiWorker(urllib2.Request):

    __APIKEY__ = 'e5c765758a'
    __APIURL__ = 'http://www.discogs.com/%(cat)s/%(val)s?f=xml&api_key=%(key)s'

    def __init__(self):
        headers = {
            'Accept-Encoding' : 'gzip'
            }

        self.opener = urllib2.build_opener()
        self.opener.addheaders = [ (k, v) for k, v in headers.iteritems() ]

    def open(self, category, value):

        if isinstance(value, basestring):
            value = urllib.quote_plus(value)

        params = {
            'cat' : category,
            'val' : value,
            'key' : self.__APIKEY__
            }

        try:
            data = self.opener.open(self.__APIURL__ % params).read()
        except urllib2.HTTPError, e:
            # Catching 'Not found' response
            if e.code == 404:
                return
            raise e

        fileobj = fileobj=cStringIO.StringIO(data)
        response = gzip.GzipFile(fileobj=fileobj).read()
        if not re.match(r'^<resp stat="ok".*$', response):
            return
        return response

    def getRelease(self, id, xml=False):
        type = 'release'
        response = self.open(type, id)

        if not response:
            return
        elif not xml:
            # Converting string to xml ETree
            response = lxml.etree.fromstring(response).xpath('./%s' % type)[0]

            data = {
                'id' : id,
                'images' : map(
                    lambda e: Image(e.attrib),
                    response.xpath('./images/image')
                    ),
                'labels' : map(
                    lambda e: Label(e.attrib),
                    response.xpath('./labels/label')
                    ),
                'artists' : map(
                    lambda e: tree2object(e, Artist, type='Release'),
                    response.xpath('./artists/artist')
                    ),
                'extraartists' : map(
                    lambda e: tree2object(e, Artist, type='Release'),
                    response.xpath('./extraartists/artist')
                    ),
                # TODO: formats parsing
                'formats' : None,
                'genres' : tree2list(
                    response.xpath('./genres/genre')
                    ),
                'styles' : tree2list(
                    response.xpath('./styles/style')
                    ),
                'tracklist' : map(
                    lambda e: tree2object(e, Track),
                    response.xpath('./tracklist/track')
                    )
                }

            # Processing tags with no children
            for k in ('title', 'released', 'country', 'notes'):
                data[k] = response.xpath('./%s' % k)[0].text

            return Release(data)
        else:
            return response

    def getArtist(self, name, xml=False):
        type = 'artist'
        response = self.open(type, name)

        if not response:
            return
        elif not xml:
            # Converting string to xml ETree
            response = lxml.etree.fromstring(response).xpath('./%s' % type)[0]

            data = {
                'images' : map(
                    lambda e: Image(e.attrib),
                    response.xpath('./images/image')
                    ),
                'urls' : tree2list(
                    response.xpath('./urls/url')
                    ),
                'namevariations' : tree2list(
                    response.xpath('./namevariations/name')
                    ),
                'members' : tree2list(
                    response.xpath('./members/name')
                    ),
                'aliases' : tree2list(
                    response.xpath('./aliases/name')
                    ),
                'releases' : map(
                    lambda e: tree2object(e, Release, type='Artist'),
                    response.xpath('./releases/release')
                )
            }

            # Processing tags with no children
            for k in ('name', 'realname', ):
                data[k] = response.xpath('./%s' % k)[0].text

            return Artist(data)
        else:
            return response

    def getLabel(self, name, xml=False):
        type = 'label'
        response = self.open(type, name)

        if not response:
            return
        elif not xml:
            # Converting string to xml ETree
            response = lxml.etree.fromstring(response).xpath('./%s' % type)[0]

            data = {
                'images' : map(
                    lambda e: Image(e.attrib),
                    response.xpath('./images/image')
                    ),
                'sublabels' : tree2list(
                    response.xpath('./sublabels/label')
                    ),
                'urls' : tree2list(
                    response.xpath('./urls/url')
                    ),
                'releases' : map(
                    lambda e: tree2object(e, Release, type='Label'),
                    response.xpath('./releases/release')
                )
            }

            # Processing tags with no children
            for k in ('name', 'contactinfo', 'profile'):
                data[k] = response.xpath('./%s' % k)[0].text

            return Label(data)
        else:
            return response

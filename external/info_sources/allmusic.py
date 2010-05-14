#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Tellico Data Source script for allmusic.com
#
# Copyright (C) 2008 by Ivo van Poorten
#
# Based on fr.allocine script by Mathias Monnerville, Copyright (C) 2006
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.

import sys, os, re, md5, random, urllib, urllib2, time, base64, xml.dom.minidom
import socket, optparse

XML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>"""
DOCTYPE = """<!DOCTYPE tellico PUBLIC "-//Robby Stephenson/DTD Tellico V9.0//EN" "http://periapsis.org/tellico/dtd/v9/tellico.dtd">"""
VERSION = "0.4"

# -----------------------------------------------------------------------------

def genMD5():
    obj = md5.new()
    obj.update(str(random.random()))
    return obj.hexdigest()

# -----------------------------------------------------------------------------

class BasicTellicoDOM:
    def __init__(self):
        self.__doc = xml.dom.minidom.Document()
        self.__root = self.__doc.createElement('tellico')
        self.__root.setAttribute('xmlns', 'http://periapsis.org/tellico/')
        self.__root.setAttribute('syntaxVersion', '9')
        
        self.__collection = self.__doc.createElement('collection')
        self.__collection.setAttribute('title', 'My Music')
        self.__collection.setAttribute('type', '4')
        
        self.__fields = self.__doc.createElement('fields')
        self.__dfltField = self.__doc.createElement('field')
        self.__dfltField.setAttribute('name', '_default')
        
        self.__customField = self.__doc.createElement('field')
        self.__customField.setAttribute('flags', '0')
        self.__customField.setAttribute('title', 'AMG URL')
        self.__customField.setAttribute('category', 'General')
        self.__customField.setAttribute('format', '4')
        self.__customField.setAttribute('type', '7')
        self.__customField.setAttribute('name', 'amg-url')

        self.__fields.appendChild(self.__dfltField)
        self.__fields.appendChild(self.__customField)
        self.__collection.appendChild(self.__fields)

        self.__images = self.__doc.createElement('images')

        self.__root.appendChild(self.__collection)
        self.__doc.appendChild(self.__root)

        self.__currentId = 0

    def addNode(self, toNode, element, text):
        node = self.__doc.createElement(element)
        node.appendChild(self.__doc.createTextNode(unicode(text, 'latin-1').encode('utf-8')))
        toNode.appendChild(node)

    def addEntry(self, data):
        entryNode = self.__doc.createElement('entry')
        entryNode.setAttribute('id', str(self.__currentId))

        for i in ('artist', 'title', 'year', 'label', 'medium', 'amg-url'):
            self.addNode(entryNode, i, data[i])

        genresNode = self.__doc.createElement('genres')
        for i in data['genre']:
            self.addNode(genresNode, 'genre', i)
        entryNode.appendChild(genresNode)

        tracksNode = self.__doc.createElement('tracks')
        for i in data['track']:
            trackNode = self.__doc.createElement('track')
            self.addNode(trackNode, 'column', i[0])
            self.addNode(trackNode, 'column', data['artist'])
            self.addNode(trackNode, 'column', i[1])
            tracksNode.appendChild(trackNode)
        entryNode.appendChild(tracksNode)

        if data['cover']:
            imageNode = self.__doc.createElement('image')
            imageNode.setAttribute('format', 'JPEG')
            imageNode.setAttribute('id', data['cover'][0])
            imageNode.appendChild(self.__doc.createTextNode(unicode(data['cover'][1], 'latin-1').encode('utf-8')))
            self.__images.appendChild(imageNode)
            self.addNode(entryNode, 'cover', data['cover'][0])

        self.__collection.appendChild(entryNode)
        self.__currentId += 1

    def printXML(self):
        self.__collection.appendChild(self.__images)
        print XML_HEADER
        print DOCTYPE
        print self.__root.toxml()

# -----------------------------------------------------------------------------

class WebsiteParser:
    def __init__(self):
        self.__baseURL  = 'http://www.allmusic.com/'
        self.__searchURL= 'http://www.allmusic.com/cg/amg.dll?p=amg&opt1=2&sql='
        self.__infoURL  = 'http://www.allmusic.com/cg/amg.dll?p=amg&'
        self.__lastURL  = ''
        self.__retry    = 3
        self.__timeout  = 10
        self.__domTree  = BasicTellicoDOM()
        self.__medium   = 'Compact Disc'
        self.__numhits  = 3
        self.__covers   = True

        self.__regExps = {
                'artist'    : 'sql=11:\w*">(?P<artist>.*?)</a>',
                'title'     : 'Album</span>.*?left:5px;"> (?P<title>.*?)</td>',
                'year'      : 'Release Date</span>.*?left:5px;">.*?(?P<year>....)</td>',
                'label'     : 'Label</span>.*?left:5px;">(?P<label>.*?)</td>',
                'genre'     : 'Genre Listing-->(?P<genre>.*?)--End Genre',
                'track'     : '(?P<track>cell">1.*?)Releases',
                'cover'     : 'Album Photo.*?src="(?P<cover>.*?jpg)"'
                }

    def setMedium(self, medium):
        self.__medium = medium

    def setTimeout(self, timeout):
        self.__timeout = timeout

    def setRetry(self, retry):
        self.__retry = retry

    def setNumhits(self, numhits):
        self.__numhits = numhits

    def setCovers(self, covers):
        self.__covers = covers

    def __getBinaryContent(self, url):
        retry = self.__retry
        while retry > 0 :
            try:
                u = urllib2.urlopen(url)
                d = u.read()
                u.close()
                return d
            except:
                retry -= 1
        print "Network Error"
        sys.exit(1)

    def __getHTMLContent(self, url):
        self.__lastURL = url
        self.__data = self.__getBinaryContent(url)
        self.__data = re.sub('&amp;amp;', '&', self.__data)
        self.__data = re.sub('&amp;', '&', self.__data)

    def __getHits(self, title):
        if not len(title): return
        self.__getHTMLContent(self.__searchURL + urllib.quote(title))
        temp = re.findall(r'\bsql=10:\w*', self.__data)
        temp = [x for x in temp if x not in locals()['_[1]']]
        self.__hits = []
        for i in range(0,self.__numhits):
            self.__hits.append(self.__infoURL + temp[i])

    def __parseInfo(self):
        data = {}
        data['medium'] = self.__medium
        data['amg-url'] = self.__lastURL

        for name, regexp in self.__regExps.iteritems():
            match = re.search(regexp, self.__data, re.DOTALL)
            data[name]=''
            if match:
                if name == 'genre':
                    data[name] = []
                    genresList = re.findall('sql=.*?>(?P<genre>.*?)</a', match.group(name))
                    for g in genresList:
                        data[name].append(g.strip())
                elif name == 'track':
                    data[name] = []
                    # first check if there are lengths available, otherwise
                    # re.findall will take ages!
                    if re.findall('^(?P<length>\d+:\d\d)\s*$', match.group(name), re.M) != [] :
                        tracksList = re.findall('cell">\d.*?sql=33:.*?>(?P<track>.*?)<.*?(?P<length>\d+:\d\d)', match.group(name), re.DOTALL)
                    else:
                        tracksList = re.findall('cell">\d.*?sql=33:.*?>(?P<track>.*?)<(?P<dummy>)', match.group(name), re.DOTALL)

                    for t in tracksList:
                        data[name].append(t)
                elif name == 'cover':
                    if self.__covers:
                        img = self.__getBinaryContent(match.group(name))
                        data[name] = (genMD5() + '.jpg', base64.encodestring(img))
                else:
                    data[name] = match.group(name).strip()

        return data

    def searchTitle(self, title):
        self.__getHits(title)
        for url in self.__hits:
            self.__getHTMLContent(url)
            self.__domTree.addEntry(self.__parseInfo())
        self.__domTree.printXML()

    def fastSearchTitle(self, title):
        if not len(title): return
        self.__getHTMLContent(self.__searchURL + urllib.quote(title))
        temp = re.findall(r'trlink".*?"cell">(?P<year>\d\d\d\d).*?word;">(?P<artist>.*?)</TD.*?(?P<link>sql=10:.*?)">(?P<title>.*?)</.*?-word;">(?P<label>.*?)</', self.__data)
        hitList = []
        for i in range(0,min(self.__numhits,len(temp))):
            hitList.append(temp[i])
        data = {}
        data['medium'] = self.__medium
        data['genre'] = data['track'] = data['cover'] = ''
        for h in hitList:
            data['year'] = h[0]
            data['artist'] = h[1]
            data['amg-url'] = self.__infoURL + h[2]
            data['title'] = h[3]
            data['label'] = h[4]
            self.__domTree.addEntry(data)
        self.__domTree.printXML()

    def updateURL(self, url):
        self.__getHTMLContent(url)
        self.__domTree.addEntry(self.__parseInfo())
        self.__domTree.printXML()

# -----------------------------------------------------------------------------

def main():
    p = optparse.OptionParser(version="%prog 0.9")
    p.add_option("-m", "--medium", dest="medium", default="Compact Disc", help="set medium for each entry", metavar="Compact Disc|Vinyl|Cassette|DVD")
    p.add_option("-t", "--timeout", type="float", dest="timeout", default=10, metavar="SECONDS", help="set socket timeout")
    p.add_option("-r", "--retry", dest="retry", type="int", default=3, help="set number of retries for each connection", metavar="NUMBER")
    p.add_option("-n", "--number-of-hits", type="int", dest="numhits", default=3, help="set the number of hits returned", metavar="NUMBER")
    p.add_option("-c", "--no-covers", action="store_false", dest="covers", default="True", help="do not download covers")
    p.add_option("-f", "--fast", action="store_true", dest="fast", default="False", help="fast album title search (limited information)")
    p.add_option("-a", "--album-title", dest="title", default='', help="search album title")
    p.add_option("-u", "--update-url", dest="url", default='', help="update from amg url")

    (options, args) = p.parse_args()

    w = WebsiteParser()
    w.setMedium(options.medium)
    w.setRetry(options.retry)
    w.setNumhits(options.numhits)
    w.setCovers(options.covers)
    socket.setdefaulttimeout(options.timeout)

    if args != []:
        p.parse_args(['-h'])

    if options.title != '':
        if options.fast:
            w.fastSearchTitle(options.title)
        else:
            w.searchTitle(options.title)
    elif options.url != '':
        w.updateURL(options.url)
    else:
        p.parse_args(['-h'])

if __name__ == '__main__':
    main()

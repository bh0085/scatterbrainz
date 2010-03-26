# -*- coding: utf-8 -*-

import re
import sys
import unittest

from urllib2 import HTTPError

sys.path.append('../')

from discogs import ApiWorker, _LoadableObject
from discogs import Image, Label, Artist, Track, Release

class TestApiWorker(unittest.TestCase):
    def setUp(self):
        self.aw = ApiWorker()

    def test_open(self):
        response = self.aw.open('release', '1')
        self.failUnless(response)
        self.failUnlessEqual(type(response), str)
        self.failUnless(
            re.search(r'<resp stat="ok"', response)
            )

        try:
            response = self.aw.open('release', '999999999999')
        except HTTPError, e:
            if e.code == 404:
                self.fail('Not found error should be catched')
            else:
                pass

    def test_getRelease(self):
        r = self.aw.getRelease(1)
        self.failUnlessEqual(r.id, 1)

        self.failUnlessEqual(len(r.images), 4)
        for i in r.images:
            self.failUnless(isinstance(i, Image))

        self.failUnlessEqual(i.type, 'secondary')
        self.failUnlessEqual(i.width, '600')
        self.failUnlessEqual(i.height, '600')
        self.failUnlessEqual(i.uri, 'http://www.discogs.com/image/R-1-1193812091.jpeg')
        self.failUnlessEqual(i.uri150, 'http://www.discogs.com/image/R-150-1-1193812091.jpeg')

        for a in r.artists:
            self.failUnless(isinstance(a, Artist))

        self.failUnlessEqual(a.name, 'Persuader, The')
        self.failUnlessEqual(a.role, None)

        for l in r.labels:
            self.failUnless(isinstance(l, Label))

        self.failUnlessEqual(l.catno, 'SK032')
        self.failUnlessEqual(l.name, 'Svek')

        for a in r.extraartists:
            self.failUnless(isinstance(a, Artist))

        self.failUnlessEqual(a.name, u'Jesper Dahlbäck')
        self.failUnlessEqual(a.role, 'Producer, Written-By')

        self.failUnlessEqual(r.genres, ['Electronic', ])
        self.failUnlessEqual(r.styles, ['Deep House', ])
        self.failUnlessEqual(r.title, 'Stockholm')
        self.failUnlessEqual(r.country, 'Sweden')
        self.failUnlessEqual(r.released, '1999-03-00')
        self.failUnlessEqual(r.notes, 'The titles are the names of Stockholm\'s districts.')

        self.failUnlessEqual(len(r.tracklist), 6)
        for t in r.tracklist:
            self.failUnless(isinstance(t, Track))

        self.failUnlessEqual(t.position, 'D')
        self.failUnlessEqual(t.title, 'Gamla Stan')
        self.failUnlessEqual(t.duration, '5:16')

    def test_getArtist(self):
        a = self.aw.getArtist('Aphex Twin')

        for i in a.images:
            self.failUnless(isinstance(i, Image))

        self.failUnlessEqual(i.type, 'secondary')
        self.failUnlessEqual(i.width, '600')
        self.failUnlessEqual(i.height, '400')
        self.failUnlessEqual(i.uri, 'http://www.discogs.com/image/A-45-1216837292.jpeg')
        self.failUnlessEqual(i.uri150, 'http://www.discogs.com/image/A-150-45-1216837292.jpeg')

        self.failUnlessEqual(
            a.urls,
            [ 'http://www.drukqs.net',
              'http://en.wikipedia.org/wiki/Aphex_twin' ]
            )

        self.failUnlessEqual(
            a.namevariations,
            [ 'A-F-X Twin',
              'A.F.X.',
              'AFX',
              'AFX (AKA Aphex Twin)',
              'Aphex Twin, The',
              'Aphex Twins' ]
            )

        self.failUnlessEqual(
            a.aliases,
            [ 'Blue Calx (2)',
              'Bradley Strider',
              'Brian Tregaskin',
              'Caustic Window',
              'Dice Man, The',
              'GAK',
              'Karen Tregaskin',
              'Polygon Window',
              'Power-Pill',
              'Q-Chastic',
              'Richard D. James',
              'Smojphace',
              'Soit-P.P.',
              'Tuss, The' ]
            )

        for r in a.releases:
            self.failUnless(isinstance(r, Release))

        self.failUnlessEqual(r.id, '1543293')
        self.failUnlessEqual(r.status, 'Accepted')
        self.failUnlessEqual(r.type, 'UnofficialRelease')
        self.failUnlessEqual(r.title, 'XXX')
        self.failUnlessEqual(r.trackinfo, 'Icct Graft')
        self.failUnlessEqual(r.format, '12", W/Lbl, Ltd')
        self.failUnlessEqual(r.label, 'Remerge Records')
        self.failUnlessEqual(r.year, '2008')


    def test_getLabel(self):
        l = self.aw.getLabel('Bully Records')

        for i in l.images:
            self.failUnless(isinstance(i, Image))

        self.failUnlessEqual(i.type, 'secondary')
        self.failUnlessEqual(i.width, '150')
        self.failUnlessEqual(i.height, '150')
        self.failUnlessEqual(i.uri, 'http://www.discogs.com/image/L-19285-1137114854.jpeg')
        self.failUnlessEqual(i.uri150, 'http://www.discogs.com/image/L-150-19285-1137114854.jpeg')

        self.failUnlessEqual(l.sublabels, ['Bully Projects', ])
        self.failUnlessEqual(
            l.urls,
            [ 'http://www.bullyrecords.com',
              'http://www.myspace.com/bullyrecords' ]
            )
        self.failUnlessEqual(l.name, 'Bully Records')
        self.failUnlessEqual(l.contactinfo, 'info@bullyrecords.com')
        self.failUnlessEqual(l.profile, 'All Bully stuff is silk-screened by Leyla. Marco folds and numbers the records. Sixtoo does most of the layout and he also masters the recordings at his studio (or with Ryebread from SNB mastering).')

        for r in l.releases:
            self.failUnless(isinstance(r, Release))

        self.failUnlessEqual(r.id, '618708')
        self.failUnlessEqual(r.catno, 'none')
        self.failUnlessEqual(r.status, 'Accepted')
        self.failUnlessEqual(r.artist, 'Various')
        self.failUnlessEqual(r.title, 'Bully Records Ghetto Sampler')
        self.failUnlessEqual(r.format, 'CDr')

    def tearDown(self):
        pass

class Test_LoadableObject(unittest.TestCase):
    def test_load(self):
        data = {
            'attr1' : 'val1',
            'attr2' : 'val2'
            }

        lo = _LoadableObject({
            'attr1' : 'val1',
            'attr2' : 'val2'
            })

        for attr in data.iterkeys():
            try:
                getattr(lo, attr)
            except AttributeError:
                self.fail('Attribute "%s" was not set!' % s)

if __name__ == '__main__':
    unittest.main()

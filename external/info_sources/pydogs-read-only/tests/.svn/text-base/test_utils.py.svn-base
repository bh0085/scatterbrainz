# -*- coding: utf-8 -*-

import lxml.etree
import sys
import unittest

sys.path.append('../')

from discogs import tree2object, tree2list, _LoadableObject

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.xml = lxml.etree.fromstring(
        '''
        <tag attr1="value1" attr2="value2">
            <subtag1>Text1</subtag1>
            <subtag2>Text2</subtag2>
        </tag>
        '''
        )

        self.dict = {
                        'subtag1' : 'Text1',
                        'subtag2' : 'Text2',
                        'attr1' : 'value1',
                        'attr2' : 'value2'
                    }

    def test_tree2object(self):
        o = tree2object(self.xml, _LoadableObject)

        self.failUnless(o)
        self.failUnlessEqual(o.subtag1, 'Text1')
        self.failUnlessEqual(o.subtag2, 'Text2')
        self.failUnlessEqual(o.attr1, 'value1')
        self.failUnlessEqual(o.attr2, 'value2')
        self.failUnlessEqual(o._data, self.dict)

    def test_tree2list(self):
        l = tree2list(self.xml)
        self.failUnless(l)
        self.failUnlessEqual(l, [ 'Text1', 'Text2' ])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

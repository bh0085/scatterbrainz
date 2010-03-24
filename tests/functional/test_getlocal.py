from scatterbrainz.tests import *

class TestGetlocalController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='getlocal', action='index'))
        # Test response...

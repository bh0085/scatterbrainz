from scatterbrainz.tests import *

class TestPlugController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='plug', action='index'))
        # Test response...

from scatterbrainz.tests import *

class TestGetmbController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='getmb', action='index'))
        # Test response...

from scatterbrainz.tests import *

class TestInitController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='init', action='index'))
        # Test response...

from scatterbrainz.tests import *

class TestQueriesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='queries', action='index'))
        # Test response...

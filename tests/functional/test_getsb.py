from scatterbrainz.tests import *

class TestGetsbController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='getsb', action='index'))
        # Test response...

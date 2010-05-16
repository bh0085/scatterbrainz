from scatterbrainz.tests import *

class TestLoad2Controller(TestController):

    def test_index(self):
        response = self.app.get(url(controller='load2', action='index'))
        # Test response...

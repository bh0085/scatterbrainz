from scatterbrainz.tests import *

class TestHello2Controller(TestController):

    def test_index(self):
        response = self.app.get(url(controller='hello2', action='index'))
        # Test response...

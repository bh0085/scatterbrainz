from scatterbrainz.tests import *

class TestGetwhatController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='getwhat', action='index'))
        # Test response...

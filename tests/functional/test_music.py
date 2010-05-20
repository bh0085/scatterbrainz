from scatterbrainz.tests import *

class TestMusicController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='music', action='index'))
        # Test response...

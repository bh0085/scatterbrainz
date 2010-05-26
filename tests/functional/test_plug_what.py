from scatterbrainz.tests import *

class TestPlugWhatController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='plug_what', action='index'))
        # Test response...

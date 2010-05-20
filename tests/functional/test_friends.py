from scatterbrainz.tests import *

class TestFriendsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='friends', action='index'))
        # Test response...

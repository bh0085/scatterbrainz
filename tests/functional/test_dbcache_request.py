from scatterbrainz.tests import *

class TestDbcacheRequestController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dbcache_request', action='index'))
        # Test response...

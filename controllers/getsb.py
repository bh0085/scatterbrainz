import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

import simplejson as sjson

log = logging.getLogger(__name__)
import pgdb
from pg import OperationalError

class GetsbController(BaseController):
    cxn = None
    #Query the centralized scatterbrainz DB
    #For now, should call _cursor and close the cursor manually when done.
    def _openCXN(self):
        GetsbController.cxn = pgdb.connect(host = "rosa.feralhosting.com:64077",
                            database = "musicbrainz_db",
                            user = "bh0085")
    def _closeCXN(self):
        print "CLOSING"
        self._cxn().close()
    def _cxn(self):
        return GetsbController.cxn
    def _cursor(self):
        print self._cxn()
        if not self._cxn():
            self._openCXN()
            print "Initializing connection"
        while True:
            try:
                cursor = self._cxn().cursor()
                break
            except OperationalError, e:
                self._openCXN()
                print "Refreshing connection"
        return cursor

    def test(self):
        sabbath_mbid ="5182c1d9-c7d2-4dad-afa0-ccfeada921a8"
        return sjson.dumps(self.getSBAlbumsForArtistMBID(sabbath_mbid))

    def requestSBArtistAlbumsForTrack(self):
        pass
        
    def getSBAlbumsForArtistMBID(self,mbid):
        cursor = self._cursor()
        cursor.execute("select id from artist where gid = '" +mbid+"';")
        artist_id = cursor.fetchone()[0]
        cursor.execute("select name, artist from album where artist = '"+unicode(artist_id)+"';")
        fetched = cursor.fetchall()
        cursor.close()
        return fetched
    

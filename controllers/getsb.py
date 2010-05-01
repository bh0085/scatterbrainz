import logging


from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render
import urllib
import simplejson as sjson

log = logging.getLogger(__name__)
import pgdb
from pg import OperationalError

class GetsbController(BaseController):
    cxn = None
    #Query the centralized scatterbrainz DB
    #For now, should call _cursor and close the cursor manually when done.

    def index(self):
        return render('/rosa_template.html')


    def demo(self):
        return render('/isdemo.html')



    def getRemoteSB(self, id):
        params = request.params
        remote_url = "http://rosa.feralhosting.com:64078/getsb/"
        if params: param_str = '?' + urllib.urlencode(params)
        else: param_str = ''
        remote_request = remote_url + id + param_str
        o = urllib.urlopen(remote_request)
        r = o.read()
        print r
        return r
        

    def test2(self):
        if 'artist' in request.params.keys():
            artist = request.params['artist']
        else:
            artist = "Black Sabbath"

        cursor = self._cursor()
        cursor.execute("select id from artist where name = '" +artist+"';")
        fetched= cursor.fetchone()
        if not fetched: return sjson.dumps('no results!')
        artist_id = fetched[0]
        cursor.execute("select name from album where artist = '"+unicode(artist_id)+"';")
        fetched = cursor.fetchall()
        cursor.close()
        j = sjson.dumps(fetched)
        return j



    def requestSBArtistAlbumsForTrack(self):
        pass
        
    def getSBAlbumsForArtistMBID(self,mbid):
        cursor = self._cursor()
        cursor.execute("select id from artist where gid = '" +mbid+"';")
        artist_id = cursor.fetchone()[0]
        cursor.execute("select * from album where artist = '"+unicode(artist_id)+"';")
        fetched = cursor.fetchall()
        cursor.close()
        return fetched
    
 

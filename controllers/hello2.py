import logging
import simplejson as sjson
import os
import urllib

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.meta import Session

log = logging.getLogger(__name__)

class Hello2Controller(BaseController):

    def index(self):
        return render('/hello2.html')
    def i2(self):
        return render('/h2player.html')
    def i2g(self):
        return render('/h2grav.html')

    def pp2(self):
        artists = Session.query(Artist)
        tracks = Session.query(Track)
        paths = []
        for r in tracks:
            paths.append( os.path.join('.media', r.filepath ))
            
        return render('/hello2.html')
    
    def songTag(self):
        url = self.songAbsURL()
        tag = '<audio src='+url+' autoplay=autoplay controls=controls></audio>'
        return tag
       
    def songRelURL(self):
        tracks = Session.query(Track)
        r = tracks[0]
        path = os.path.join('.music', r.filepath )
        out =urllib.pathname2url(path)
        return out


    def songAbsURL(self):
        rel = self.songRelURL()
        abs_url = 'http://localhost:5000/'+rel
        return sjson.dumps([abs_url,abs_url])
 
    def printPaths(self):
        tracks = Session.query(Track)
        paths = []
        for r in tracks:
            paths.append( os.path.join('.media', r.filepath ))
            
        return paths
    



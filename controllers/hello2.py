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
        # Return a rendered template

                
        return render('/hello2.html')

    def pp2(self):
        artists = Session.query(Artist)
        tracks = Session.query(Track)
        paths = []
        for r in tracks:
            paths.append( os.path.join('.media', r.filepath ))
            
        return render('/hello2.html')
    
    def songTag(self):
        tracks = Session.query(Track)
        r = tracks[0]
        path = os.path.join('.music', r.filepath )
        tag = '<audio src=http://localhost:5000/'+urllib.pathname2url(path)+' autoplay=autoplay controls=controls></audio>'
        return tag
       

    def printPaths(self):
        tracks = Session.query(Track)
        paths = []
        for r in tracks:
            paths.append( os.path.join('.media', r.filepath ))
            
        return paths
    

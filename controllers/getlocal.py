import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.meta import Session
import urllib
from scatterbrainz.lib.base import BaseController, render
import os
import simplejson as sjson

log = logging.getLogger(__name__)

class GetlocalController(BaseController):

    def blah(self):
        return "HELLO"

    def alltracks(self):
        tracks = Session.query(Track)
        namefun = lambda x: x.id3title
        out = []
        for t in tracks:
            name = namefun(t)
            type = t.__class__.__name__
            json = {
                'type':type,
                'name':name,
                'url':self.track_URL_from_id(t.id),
                'id':t.id
                    }
            out.append(json)
        return sjson.dumps(out)
    
    def track_URL_from_id(self,id):
        track = Session.query(Track).filter_by(id=id)[0]
        path = os.path.join('.music',track.filepath)
        url = self._path_url(path)
        return url

    def _path_url(self, path):         
        return os.path.join('http://localhost:5000',urllib.pathname2url(path))
        

    

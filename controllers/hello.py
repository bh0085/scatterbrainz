import os
import time

import logging

import simplejson as sjson

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

from scatterbrainz.model.meta import Session
from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album

class HelloController(BaseController):
    
    def index(self):
        c.tracks = Session.query(Track)
        return render('/hello.html')

    def treebrowse(self):
        idStr = request.params['id']
        if idStr == '0':
            return self._allartists()
        else:
            [type, id] = idStr.split('/',1)
            if type == 'Artist':
                return self._albumsforartist(id)
            elif type == 'Album':
                return self._tracksforalbum(id)
    
    def _makeJSON(self, results, leaf, namefun):
        alljson = []
        for result in results:
            id = result.id
            name = namefun(result)
            type = result.__class__.__name__
            json = {
                'attributes': {'id'   : type + '/' + str(id),
                               'class': 'browsenode'
                              },
                'data': name
            }
            if not leaf:
                json['state'] = 'closed'
            alljson.append(json)
        return sjson.dumps(alljson)
    
    def _allartists(self):
        artists = Session.query(Artist)
        namefun = lambda x: x.name
        return self._makeJSON(artists, False, namefun)
    
    def _albumsforartist(self, artistid):
        albums = Session.query(Album).join(Track).filter_by(artistid=artistid)
        namefun = lambda x: x.name
        return self._makeJSON(albums, False, namefun)
    
    def _tracksforalbum(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        namefun = lambda x: x.id3title
        return self._makeJSON(tracks, True, namefun)

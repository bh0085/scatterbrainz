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
        return render('/hello.html')

    def treeBrowseAJAX(self):
        idStr = request.params['id']
        if idStr == '0':
            return self._allArtistsTreeJSON()
        else:
            [type, id] = idStr.split('/',1)
            if type == 'Artist':
                return self._albumsForArtistTreeJSON(id)
            elif type == 'Album':
                return self._tracksForAlbumTreeJSON(id)
            else:
                raise Exception('bad type '+type)
    
    def _allArtistsTreeJSON(self):
        artists = Session.query(Artist)
        namefun = lambda x: x.name
        return self._treeJSON(artists, False, namefun)
    
    def _albumsForArtistTreeJSON(self, artistid):
        albums = Session.query(Album).join(Track).filter_by(artistid=artistid)
        namefun = lambda x: x.name
        return self._treeJSON(albums, False, namefun)
    
    def _tracksForAlbumTreeJSON(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        namefun = lambda x: x.id3title
        return self._treeJSON(tracks, True, namefun)
    
    def _treeJSON(self, results, leaf, namefun):
        alljson = []
        for result in results:
            id = result.id
            name = namefun(result)
            type = result.__class__.__name__
            json = {
                'attributes': {'id'   : type + '/' + str(id),
                               'class': 'browsenode',
                               'rel'  : type
                              },
                'data': name
            }
            if not leaf:
                json['state'] = 'closed'
            alljson.append(json)
        return sjson.dumps(alljson)
    
    def getTracksAJAX(self):
        idStr = request.params['id']
        [type, id] = idStr.split('/',1)
        if type == 'Track':
            return self._trackPlaylistJSON(id)
        elif type == 'Artist':
            return self._tracksForArtistPlaylistJSON(id)
        elif type == 'Album':
            return self._tracksForAlbumPlaylistJSON(id)
        else:
            raise Exception('bad type '+type)

    def _trackPlaylistJSON(self, trackid):
        tracks = Session.query(Track).filter_by(id=trackid)
        return self._playlistJSON(tracks)
    
    def _tracksForAlbumPlaylistJSON(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        return self._playlistJSON(tracks)
    
    def _tracksForArtistPlaylistJSON(self, artistid):
        tracks = Session.query(Track).filter_by(artistid=artistid)
        return self._playlistJSON(tracks)

    def _playlistJSON(self, tracks):
        json = map(lambda x: x.toJSON(), tracks)
        return sjson.dumps(json)

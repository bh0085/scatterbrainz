import os
import time

import logging

import simplejson

from sqlalchemy.orm import contains_eager

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

from scatterbrainz.external.my_MB import getRelease, searchRelease

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
        if idStr == 'init':
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
        return self._dumpFlatJSON(artists)
    
    def _albumsForArtistTreeJSON(self, artistid):
        albums = Session.query(Album).join(Track).filter_by(artistid=artistid)
        return self._dumpFlatJSON(albums)
    
    def _tracksForAlbumTreeJSON(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        return self._dumpFlatJSON(tracks)
    
    def _dumpFlatJSON(self, results):
        json = map(lambda x: x.toTreeJSON(), results)
        return simplejson.dumps(json)
    
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
        json = map(lambda x: x.toPlaylistJSON(), tracks)
        return simplejson.dumps(json)
    
    def searchAJAX(self):
        search = request.params['search']
        maxResults = 50
        artists = Session.query(Artist). \
                         filter(Artist.name.like('%'+search+'%')) \
                         [0:maxResults]
        # this is kind of fucked, need to rethink join model
        #albums = Session.query(Album). \
        #                 filter(Artist.name.like('%'+search+'%')). \
        #                 join(Album). \
        #                 options(contains_eager(Album.tracks)) \
        #                 [0:maxResults]
        tracks = Session.query(Track). \
                         filter(Track.id3title.like('%'+search+'%')). \
                         join(Artist). \
                         join(Album) \
                         [0:maxResults]
        if len(artists) == maxResults or len(tracks) == maxResults: #or len(albums) == maxResults:
            truncated = True
        else:
            truncated = False
        json = []
        artistIdToJSON = {}
        albumsIdToJSON = {}
        for track in tracks:
            if track.artist.id not in artistIdToJSON:
                artistJSON = track.artist.toTreeJSON(children=[])
                json.append(artistJSON)
                artistIdToJSON[track.artist.id] = artistJSON
            else:
                artistJSON = artistIdToJSON[track.artist.id]
            if track.album.id not in albumsIdToJSON:
                albumJSON = track.album.toTreeJSON(children=[])
                artistJSON['children'].append(albumJSON)
                albumsIdToJSON[track.album.id] = albumJSON
            else:
                albumJSON = albumsIdToJSON[track.album.id]
            albumJSON['children'].append(track.toTreeJSON())
        for artist in artists:
            if artist.id not in artistIdToJSON:
                artistJSON = artist.toTreeJSON()
                json.append(artistJSON)
                artistIdToJSON[artist.id] = artistJSON
        return simplejson.dumps(json)
    
    def albumArtAJAX(self):
        trackid = request.params['trackid'].split('_')[1]
        track = Session.query(Track).filter_by(id=trackid).one()
        
        albumArtURL = None
        release = None
        album = track.album     
        artist = track.artist
        if album.albumArtURL:
            albumArtURL = album.albumArtURL
        elif album.mbid:
            release = getRelease(album.mbid)
        else:
            release = searchRelease(track.id3artist, track.id3album)
            if release and not album.mbid:
                album.mbid = release.id
            if release and not artist.mbid:
                artist.mbid = release.artist.id
        if release and not albumArtURL:
            asin = release.getAsin()
            if asin:
                albumArtURL = 'http://ecx.images-amazon.com/images/P/%s.jpg' % (asin)
                track.album.albumArtURL = albumArtURL
        Session.commit()
        json = {}
        if albumArtURL:
            json['albumArtURL'] = albumArtURL
        return simplejson.dumps(json)
